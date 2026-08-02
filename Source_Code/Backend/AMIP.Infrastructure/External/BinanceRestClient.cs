using System.Text.Json;
using System.Text.Json.Serialization;
using AMIP.Domain.Entities;
using AMIP.Domain.Enums;
using AMIP.Domain.Interfaces;
using Microsoft.Extensions.Logging;

namespace AMIP.Infrastructure.External;

public class BinanceRestClient(HttpClient httpClient, ILogger<BinanceRestClient> logger, IMarketDataRepository marketDataRepository)
{
    private const string BaseUrl = "https://api.binance.com/api/v3/klines";

    public async Task FetchHistoricalDataAsync(string symbol, CandleInterval interval, DateTime startTime, DateTime endTime)
    {
        string binanceInterval = GetBinanceInterval(interval);
        long startTimeMs = ((DateTimeOffset)startTime).ToUnixTimeMilliseconds();
        long endTimeMs = ((DateTimeOffset)endTime).ToUnixTimeMilliseconds();

        string url = $"{BaseUrl}?symbol={symbol}&interval={binanceInterval}&startTime={startTimeMs}&endTime={endTimeMs}&limit=1000";
        
        logger.LogInformation("Fetching from Binance: {Url}", url);
        
        var response = await httpClient.GetAsync(url);
        response.EnsureSuccessStatusCode();

        var jsonStr = await response.Content.ReadAsStringAsync();
        var data = JsonSerializer.Deserialize<JsonElement[][]>(jsonStr);
        
        if (data != null)
        {
            var candles = data.Select(kline => new MarketCandle
            {
                Exchange = ExchangeType.Binance,
                Symbol = symbol,
                Interval = interval,
                OpenTime = DateTimeOffset.FromUnixTimeMilliseconds(kline[0].GetInt64()).UtcDateTime,
                Open = decimal.Parse(kline[1].GetString()!),
                High = decimal.Parse(kline[2].GetString()!),
                Low = decimal.Parse(kline[3].GetString()!),
                Close = decimal.Parse(kline[4].GetString()!),
                Volume = decimal.Parse(kline[5].GetString()!),
                CloseTime = DateTimeOffset.FromUnixTimeMilliseconds(kline[6].GetInt64()).UtcDateTime
            }).ToList();

            await marketDataRepository.SaveCandlesAsync(candles);
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
