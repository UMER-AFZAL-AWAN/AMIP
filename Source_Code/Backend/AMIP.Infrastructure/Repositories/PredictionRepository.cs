using AMIP.Domain.Entities;
using AMIP.Domain.Interfaces;
using AMIP.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

namespace AMIP.Infrastructure.Repositories;

public class PredictionRepository(AmipDbContext context) : IPredictionRepository
{
    public async Task<ModelPrediction?> GetLatestPredictionAsync(string symbol)
    {
        return await context.ModelPredictions
            .Where(x => x.Symbol == symbol)
            .OrderByDescending(x => x.Timestamp)
            .FirstOrDefaultAsync();
    }

    public async Task<IEnumerable<ModelPrediction>> GetPredictionHistoryAsync(string symbol, DateTime from, DateTime to)
    {
        return await context.ModelPredictions
            .Where(x => x.Symbol == symbol && x.Timestamp >= from && x.Timestamp <= to)
            .OrderBy(x => x.Timestamp)
            .ToListAsync();
    }

    public async Task SavePredictionAsync(ModelPrediction prediction)
    {
        context.ModelPredictions.Add(prediction);
        await context.SaveChangesAsync();
    }
}
