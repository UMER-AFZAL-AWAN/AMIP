using AMIP.Domain.Interfaces;
using AMIP.Infrastructure.Services;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace AMIP.Api.Services;

public class MarketDataHostedService(IServiceProvider serviceProvider, ILogger<MarketDataHostedService> logger) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        logger.LogInformation("MarketDataHostedService is starting.");

        // Wait a few seconds to let the application start up fully
        await Task.Delay(TimeSpan.FromSeconds(5), stoppingToken);

        try
        {
            using var scope = serviceProvider.CreateScope();
            var ingestionService = scope.ServiceProvider.GetRequiredService<IMarketDataIngestionService>();

            // Kick off the realtime stream in the background
            await ingestionService.StartRealtimeStreamAsync("BTCUSDT", "OneMinute");
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "An error occurred in MarketDataHostedService");
        }
    }
}
