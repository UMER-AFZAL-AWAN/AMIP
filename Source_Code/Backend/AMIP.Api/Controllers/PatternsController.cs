using AMIP.Domain.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace AMIP.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class PatternsController(IPatternRepository patternRepository) : ControllerBase
{
    [HttpGet("similar")]
    public async Task<IActionResult> GetSimilar([FromQuery] string symbol, [FromQuery] int limit = 5)
    {
        var patterns = await patternRepository.GetSimilarPatternsAsync(symbol, limit);
        return Ok(patterns);
    }
}
