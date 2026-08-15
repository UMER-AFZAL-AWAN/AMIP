using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using AMIP.Domain.Entities;
using AMIP.Domain.Enums;
using AMIP.Domain.Interfaces;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

namespace AMIP.Infrastructure.External;

public class BinanceWebSocketClient(ILogger<BinanceWebSocketClient> logger, IServiceScopeFactory scopeFactory)
{
    private const string BaseWsUrl = "wss://stream.binance.com:9443/ws";

    public async Task StartRealtimeStreamAsync(string symbol, CandleInterval interval, CancellationToken cancellationToken)
    {
        string binanceInterval = GetBinanceInterval(interval);
        string streamName = $"{symbol.ToLower()}@kline_{binanceInterval}";
        string url = $"{BaseWsUrl}/{streamName}";

        using var webSocket = new ClientWebSocket();
        try
        {
            logger.LogInformation("Connecting to Binance WebSocket: {Url}", url);
            await webSocket.ConnectAsync(new Uri(url), cancellationToken);
            logger.LogInformation("Connected to Binance WebSocket");

            var buffer = new byte[1024 * 4];

            while (webSocket.State == WebSocketState.Open && !cancellationToken.IsCancellationRequested)
            {
                var result = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), cancellationToken);
                
                if (result.MessageType == WebSocketMessageType.Close)
                {
                    logger.LogInformation("Binance WebSocket closed by server.");
                    await webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Server closed", cancellationToken);
                    break;
                }

                var jsonStr = Encoding.UTF8.GetString(buffer, 0, result.Count);
                await ProcessMessageAsync(jsonStr, symbol, interval);
            }
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Error in Binance WebSocket stream for {Symbol}", symbol);
            throw;
        }
    }

    private async Task ProcessMessageAsync(string jsonStr, string symbol, CandleInterval interval)
    {
        try
        {
            using var doc = JsonDocument.Parse(jsonStr);
            var root = doc.RootElement;

            if (root.TryGetProperty("k", out var kline))
            {
                var isClosed = kline.GetProperty("x").GetBoolean();
                if (isClosed)
                {
                    var candle = new MarketCandle
                    {
                        Exchange = ExchangeType.Binance,
                        Symbol = symbol,
                        Interval = interval,
                        OpenTime = DateTimeOffset.FromUnixTimeMilliseconds(kline.GetProperty("t").GetInt64()).UtcDateTime,
                        Open = decimal.Parse(kline.GetProperty("o").GetString()!),
                        High = decimal.Parse(kline.GetProperty("h").GetString()!),
                        Low = decimal.Parse(kline.GetProperty("l").GetString()!),
                        Close = decimal.Parse(kline.GetProperty("c").GetString()!),
                        Volume = decimal.Parse(kline.GetProperty("v").GetString()!),
                        CloseTime = DateTimeOffset.FromUnixTimeMilliseconds(kline.GetProperty("T").GetInt64()).UtcDateTime
                    };

                    using var scope = scopeFactory.CreateScope();
                    var marketDataRepository = scope.ServiceProvider.GetRequiredService<IMarketDataRepository>();

                    await marketDataRepository.SaveCandlesAsync(new List<MarketCandle> { candle });
                    logger.LogInformation("Saved closed candle for {Symbol} at {Time}", symbol, candle.CloseTime);
                }
            }
        }
        catch (Exception ex)
        {
            logger.LogWarning(ex, "Failed to parse or save Binance WebSocket message.");
        }
    }

    private string GetBinanceInterval(CandleInterval interval) => interval switch
    {
        CandleInterval.OneMinute => "1m",
        CandleInterval.FiveMinutes => "5m",
        CandleInterval.FifteenMinutes => "15m",
        CandleInterval.OneHour => "1h",
        CandleInterval.FourHours => "4h",
        CandleInterval.OneDay => "1d",
        _ => throw new ArgumentOutOfRangeException()
    };
}
