using AMIP.Domain.Entities;
using AMIP.Domain.Interfaces;
using AMIP.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

namespace AMIP.Infrastructure.Repositories;

public class ExperimentRepository(AmipDbContext context) : IExperimentRepository
{
    public async Task<IEnumerable<Experiment>> GetAllExperimentsAsync()
    {
        return await context.Experiments.ToListAsync();
    }

    public async Task SaveExperimentAsync(Experiment experiment)
    {
        context.Experiments.Add(experiment);
        await context.SaveChangesAsync();
    }
}
