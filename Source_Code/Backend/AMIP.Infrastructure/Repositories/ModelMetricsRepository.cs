using AMIP.Domain.Entities;
using AMIP.Domain.Interfaces;
using AMIP.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

namespace AMIP.Infrastructure.Repositories;

public class ModelMetricsRepository(AmipDbContext context) : IModelMetricsRepository
{
    public async Task<ModelMetrics?> GetMetricsAsync(string modelName)
    {
        return await context.ModelMetrics
            .Where(x => x.ModelName == modelName)
            .OrderByDescending(x => x.EvaluatedAt)
            .FirstOrDefaultAsync();
    }

    public async Task SaveMetricsAsync(ModelMetrics metrics)
    {
        context.ModelMetrics.Add(metrics);
        await context.SaveChangesAsync();
    }
}
