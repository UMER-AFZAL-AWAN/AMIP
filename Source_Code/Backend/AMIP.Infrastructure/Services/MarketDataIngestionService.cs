using AMIP.Domain.Interfaces;

namespace AMIP.Infrastructure.Services;

public class MarketDataIngestionService(BinanceRestClient binanceRestClient) : IMarketDataIngestionService
{
    public async Task IngestHistoricalDataAsync(string symbol, string interval)
    {
        // For simplicity, fetch the last 30 days
        var endTime = DateTime.UtcNow;
        var startTime = endTime.AddDays(-30);
        
        var parsedInterval = Enum.Parse<AMIP.Domain.Enums.CandleInterval>(interval, true);
        
        await binanceRestClient.FetchHistoricalDataAsync(symbol, parsedInterval, startTime, endTime);
    }

    public Task StartRealtimeStreamAsync(string symbol, string interval)
    {
        // Real-time stream to be implemented
        return Task.CompletedTask;
    }
}
