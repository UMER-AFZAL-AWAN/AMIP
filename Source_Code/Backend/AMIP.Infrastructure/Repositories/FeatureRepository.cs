using AMIP.Domain.Entities;
using AMIP.Domain.Interfaces;
using AMIP.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

namespace AMIP.Infrastructure.Repositories;

public class FeatureRepository(AmipDbContext context) : IFeatureRepository
{
    public async Task<IEnumerable<MarketFeature>> GetFeaturesAsync(string symbol, DateTime from, DateTime to)
    {
        return await context.MarketFeatures
            .Where(x => x.Symbol == symbol && x.Timestamp >= from && x.Timestamp <= to)
            .OrderBy(x => x.Timestamp)
            .ToListAsync();
    }

    public async Task SaveFeaturesAsync(IEnumerable<MarketFeature> features)
    {
        context.MarketFeatures.AddRange(features);
        await context.SaveChangesAsync();
    }
}
