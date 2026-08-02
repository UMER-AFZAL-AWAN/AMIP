using AMIP.Domain.Interfaces;
using AMIP.Infrastructure.Data;
using AMIP.Infrastructure.External;
using AMIP.Infrastructure.Repositories;
using AMIP.Infrastructure.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace AMIP.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
    {
        services.AddDbContext<AmipDbContext>(options =>
            options.UseNpgsql(configuration.GetConnectionString("DefaultConnection")));

        services.AddHttpClient<BinanceRestClient>();
        
        services.AddScoped<IMarketDataRepository, MarketDataRepository>();
        services.AddScoped<IExperimentRepository, ExperimentRepository>();
        services.AddScoped<IFeatureRepository, FeatureRepository>();
        services.AddScoped<IModelMetricsRepository, ModelMetricsRepository>();
        services.AddScoped<IModelRegistryRepository, ModelRegistryRepository>();
        services.AddScoped<IPatternRepository, PatternRepository>();
        services.AddScoped<IPredictionRepository, PredictionRepository>();

        services.AddScoped<IMarketDataIngestionService, MarketDataIngestionService>();

        return services;
    }
}
