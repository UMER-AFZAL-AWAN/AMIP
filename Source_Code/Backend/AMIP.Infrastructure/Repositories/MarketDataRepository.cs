using AMIP.Domain.Entities;
using AMIP.Domain.Enums;
using AMIP.Domain.Interfaces;
using AMIP.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

namespace AMIP.Infrastructure.Repositories;

public class MarketDataRepository(AmipDbContext context) : IMarketDataRepository
{
    public async Task<IEnumerable<MarketCandle>> GetCandlesAsync(ExchangeType exchange, string symbol, CandleInterval interval, DateTime from, DateTime to)
    {
        return await context.MarketCandles
            .Where(x => x.Exchange == exchange && x.Symbol == symbol && x.Interval == interval && x.OpenTime >= from && x.OpenTime <= to)
            .OrderBy(x => x.OpenTime)
            .ToListAsync();
    }

    public async Task<MarketCandle?> GetLatestCandleAsync(ExchangeType exchange, string symbol, CandleInterval interval)
    {
        return await context.MarketCandles
            .Where(x => x.Exchange == exchange && x.Symbol == symbol && x.Interval == interval)
            .OrderByDescending(x => x.OpenTime)
            .FirstOrDefaultAsync();
    }

    public async Task SaveCandlesAsync(IEnumerable<MarketCandle> candles)
    {
        foreach (var candle in candles)
        {
            var exists = await context.MarketCandles.AnyAsync(x => x.Exchange == candle.Exchange && x.Symbol == candle.Symbol && x.Interval == candle.Interval && x.OpenTime == candle.OpenTime);
            if (!exists)
            {
                context.MarketCandles.Add(candle);
            }
        }
        await context.SaveChangesAsync();
    }
}
