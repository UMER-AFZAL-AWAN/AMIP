using AMIP.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace AMIP.Infrastructure.Data;

public class AmipDbContext(DbContextOptions<AmipDbContext> options) : DbContext(options)
{
    public DbSet<MarketCandle> MarketCandles => Set<MarketCandle>();
    public DbSet<ProcessedCandle> ProcessedCandles => Set<ProcessedCandle>();
    public DbSet<MarketFeature> MarketFeatures => Set<MarketFeature>();
    public DbSet<MarketPattern> MarketPatterns => Set<MarketPattern>();
    public DbSet<MarketRegime> MarketRegimes => Set<MarketRegime>();
    public DbSet<ModelPrediction> ModelPredictions => Set<ModelPrediction>();
    public DbSet<ModelMetrics> ModelMetrics => Set<ModelMetrics>();
    public DbSet<Experiment> Experiments => Set<Experiment>();
    public DbSet<ModelRegistryEntry> ModelRegistryEntries => Set<ModelRegistryEntry>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
        
        modelBuilder.Entity<MarketCandle>().HasKey(x => x.Id);
        modelBuilder.Entity<MarketCandle>().HasIndex(x => new { x.Exchange, x.Symbol, x.Interval, x.OpenTime }).IsUnique();

        modelBuilder.Entity<ProcessedCandle>().HasKey(x => x.Id);
        modelBuilder.Entity<MarketFeature>().HasKey(x => x.Id);
        modelBuilder.Entity<MarketPattern>().HasKey(x => x.Id);
        modelBuilder.Entity<MarketRegime>().HasKey(x => x.Id);
        modelBuilder.Entity<ModelPrediction>().HasKey(x => x.Id);
        modelBuilder.Entity<ModelMetrics>().HasKey(x => x.Id);
        modelBuilder.Entity<Experiment>().HasKey(x => x.Id);
        modelBuilder.Entity<ModelRegistryEntry>().HasKey(x => x.Id);
    }
}
