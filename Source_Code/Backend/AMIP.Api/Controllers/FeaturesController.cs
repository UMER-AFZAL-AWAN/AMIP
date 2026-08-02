using AMIP.Domain.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace AMIP.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class FeaturesController(IFeatureRepository featureRepository) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> GetFeatures([FromQuery] string symbol, [FromQuery] string interval, [FromQuery] DateTime from, [FromQuery] DateTime to)
    {
        // For now ignoring interval as the repo is simple
        var features = await featureRepository.GetFeaturesAsync(symbol, from, to);
        return Ok(features);
    }
}
