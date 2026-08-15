using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace AMIP.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Experiments",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uuid", nullable: false),
                    Name = table.Column<string>(type: "text", nullable: false),
                    ParametersJson = table.Column<string>(type: "text", nullable: false),
                    ResultsJson = table.Column<string>(type: "text", nullable: false),
                    Conclusion = table.Column<string>(type: "text", nullable: false),
                    CreatedAt = table.Column<DateTime>(type: "timestamp with time zone", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Experiments", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "MarketCandles",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uuid", nullable: false),
                    Exchange = table.Column<int>(type: "integer", nullable: false),
                    Symbol = table.Column<string>(type: "text", nullable: false),
                    Interval = table.Column<int>(type: "integer", nullable: false),
                    OpenTime = table.Column<DateTime>(type: "timestamp with time zone", nullable: false),
                    CloseTime = table.Column<DateTime>(type: "timestamp with time zone", nullable: false),
                    Open = table.Column<decimal>(type: "numeric", nullable: false),
                    High = table.Column<decimal>(type: "numeric", nullable: false),
                    Low = table.Column<decimal>(type: "numeric", nullable: false),
                    Close = table.Column<decimal>(type: "numeric", nullable: false),
                    Volume = table.Column<decimal>(type: "numeric", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_MarketCandles", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "MarketFeatures",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uuid", nullable: false),
                    Symbol = table.Column<string>(type: "text", nullable: false),
                    Timestamp = table.Column<DateTime>(type: "timestamp with time zone", nullable: false),
                    FeatureDataJson = table.Column<string>(type: "text", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_MarketFeatures", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "MarketPatterns",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uuid", nullable: false),
                    PatternId = table.Column<string>(type: "text", nullable: false),
                    EmbeddingJson = table.Column<string>(type: "text", nullable: false),
                    ClusterId = table.Column<int>(type: "integer", nullable: false),
                    SuccessRate = table.Column<decimal>(type: "numeric", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_MarketPatterns", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "MarketRegimes",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uuid", nullable: false),
                    RegimeLabel = table.Column<int>(type: "integer", nullable: false),
                    Probability = table.Column<decimal>(type: "numeric", nullable: false),
                    ModelVersion = table.Column<string>(type: "text", nullable: false),
                    Symbol = table.Column<string>(type: "text", nullable: false),
                    Timestamp = table.Column<DateTime>(type: "timestamp with time zone", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_MarketRegimes", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "ModelMetrics",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uuid", nullable: false),
                    ModelName = table.Column<string>(type: "text", nullable: false),
                    Accuracy = table.Column<decimal>(type: "numeric", nullable: false),
                    Precision = table.Column<decimal>(type: "numeric", nullable: false),
                    Recall = table.Column<decimal>(type: "numeric", nullable: false),
                    SharpeRatio = table.Column<decimal>(type: "numeric", nullable: false),
                    MaxDrawdown = table.Column<decimal>(type: "numeric", nullable: false),
                    EvaluatedAt = table.Column<DateTime>(type: "timestamp with time zone", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_ModelMetrics", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "ModelPredictions",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uuid", nullable: false),
                    Direction = table.Column<int>(type: "integer", nullable: false),
                    UpProbability = table.Column<decimal>(type: "numeric", nullable: false),
                    DownProbability = table.Column<decimal>(type: "numeric", nullable: false),
                    NeutralProbability = table.Column<decimal>(type: "numeric", nullable: false),
                    Confidence = table.Column<decimal>(type: "numeric", nullable: false),
                    Risk = table.Column<decimal>(type: "numeric", nullable: false),
                    ActualResult = table.Column<int>(type: "integer", nullable: true),
                    Symbol = table.Column<string>(type: "text", nullable: false),
                    Timestamp = table.Column<DateTime>(type: "timestamp with time zone", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_ModelPredictions", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "ModelRegistryEntries",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uuid", nullable: false),
                    Name = table.Column<string>(type: "text", nullable: false),
                    Version = table.Column<string>(type: "text", nullable: false),
                    ModelPath = table.Column<string>(type: "text", nullable: false),
                    Status = table.Column<int>(type: "integer", nullable: false),
                    RegisteredAt = table.Column<DateTime>(type: "timestamp with time zone", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_ModelRegistryEntries", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "ProcessedCandles",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uuid", nullable: false),
                    MarketCandleId = table.Column<Guid>(type: "uuid", nullable: false),
                    IsValidated = table.Column<bool>(type: "boolean", nullable: false),
                    NormalizedOpen = table.Column<decimal>(type: "numeric", nullable: false),
                    NormalizedHigh = table.Column<decimal>(type: "numeric", nullable: false),
                    NormalizedLow = table.Column<decimal>(type: "numeric", nullable: false),
                    NormalizedClose = table.Column<decimal>(type: "numeric", nullable: false),
                    NormalizedVolume = table.Column<decimal>(type: "numeric", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_ProcessedCandles", x => x.Id);
                });

            migrationBuilder.CreateIndex(
                name: "IX_MarketCandles_Exchange_Symbol_Interval_OpenTime",
                table: "MarketCandles",
                columns: new[] { "Exchange", "Symbol", "Interval", "OpenTime" },
                unique: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Experiments");

            migrationBuilder.DropTable(
                name: "MarketCandles");

            migrationBuilder.DropTable(
                name: "MarketFeatures");

            migrationBuilder.DropTable(
                name: "MarketPatterns");

            migrationBuilder.DropTable(
                name: "MarketRegimes");

            migrationBuilder.DropTable(
                name: "ModelMetrics");

            migrationBuilder.DropTable(
                name: "ModelPredictions");

            migrationBuilder.DropTable(
                name: "ModelRegistryEntries");

            migrationBuilder.DropTable(
                name: "ProcessedCandles");
        }
    }
}
