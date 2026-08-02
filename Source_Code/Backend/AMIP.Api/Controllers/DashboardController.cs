using Microsoft.AspNetCore.Mvc;

namespace AMIP.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class DashboardController : ControllerBase
{
    [HttpGet("summary")]
    public IActionResult GetSummary()
    {
        return Ok(new 
        { 
            ActiveModels = 3,
            TotalPredictions = 15000,
            OverallAccuracy = 0.65,
            LatestRegime = "Bullish"
        });
    }
}
