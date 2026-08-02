using AMIP.Domain.Entities;
using AMIP.Domain.Interfaces;
using AMIP.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

namespace AMIP.Infrastructure.Repositories;

public class ModelRegistryRepository(AmipDbContext context) : IModelRegistryRepository
{
    public async Task<IEnumerable<ModelRegistryEntry>> GetAllEntriesAsync()
    {
        return await context.ModelRegistryEntries.ToListAsync();
    }

    public async Task SaveEntryAsync(ModelRegistryEntry entry)
    {
        context.ModelRegistryEntries.Add(entry);
        await context.SaveChangesAsync();
    }
}
