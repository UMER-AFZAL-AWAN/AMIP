using AMIP.Domain.Interfaces;
using AMIP.Infrastructure.External;

namespace AMIP.Infrastructure.Services;

public class MarketDataIngestionService(BinanceRestClient binanceRestClient, BinanceWebSocketClient binanceWebSocketClient) : IMarketDataIngestionService
{
    public async Task IngestHistoricalDataAsync(string symbol, string interval)
    {
        // For simplicity, fetch the last 30 days
        var endTime = DateTime.UtcNow;
        var startTime = endTime.AddDays(-30);
        
        var parsedInterval = Enum.Parse<AMIP.Domain.Enums.CandleInterval>(interval, true);
        
        await binanceRestClient.FetchHistoricalDataAsync(symbol, parsedInterval, startTime, endTime);
    }

    public async Task StartRealtimeStreamAsync(string symbol, string interval)
    {
        var parsedInterval = Enum.Parse<AMIP.Domain.Enums.CandleInterval>(interval, true);
        
        // This will block while running; typically called from a HostedService
        await binanceWebSocketClient.StartRealtimeStreamAsync(symbol, parsedInterval, CancellationToken.None);
    }
}
