using AMIP.Domain.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace AMIP.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ModelsController(IModelMetricsRepository metricsRepository, IModelRegistryRepository registryRepository) : ControllerBase
{
    [HttpGet("metrics")]
    public async Task<IActionResult> GetMetrics([FromQuery] string modelName)
    {
        var metrics = await metricsRepository.GetMetricsAsync(modelName);
        if (metrics == null) return NotFound();
        return Ok(metrics);
    }

    [HttpGet("registry")]
    public async Task<IActionResult> GetRegistry()
    {
        var registry = await registryRepository.GetAllEntriesAsync();
        return Ok(registry);
    }
}
