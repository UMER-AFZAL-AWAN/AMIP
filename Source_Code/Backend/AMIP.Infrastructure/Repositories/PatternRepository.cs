using AMIP.Domain.Entities;
using AMIP.Domain.Interfaces;
using AMIP.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

namespace AMIP.Infrastructure.Repositories;

public class PatternRepository(AmipDbContext context) : IPatternRepository
{
    public async Task<IEnumerable<MarketPattern>> GetSimilarPatternsAsync(string symbol, int limit)
    {
        return await context.MarketPatterns.Take(limit).ToListAsync();
    }

    public async Task SavePatternAsync(MarketPattern pattern)
    {
        context.MarketPatterns.Add(pattern);
        await context.SaveChangesAsync();
    }
}
