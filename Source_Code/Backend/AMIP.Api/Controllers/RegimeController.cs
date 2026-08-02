using AMIP.Domain.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace AMIP.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class RegimeController : ControllerBase
{
    // Need a repository for Regime in real life, returning empty/dummy for now as per requirements
    [HttpGet("current")]
    public IActionResult GetCurrent([FromQuery] string symbol)
    {
        return Ok(new { Symbol = symbol, Regime = "StrongUptrend", Probability = 0.85 });
    }

    [HttpGet("history")]
    public IActionResult GetHistory([FromQuery] string symbol, [FromQuery] DateTime from, [FromQuery] DateTime to)
    {
        return Ok(new List<object>());
    }
}
