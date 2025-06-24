using System.Text.Json.Serialization;

namespace MonitoringApi.DTOs
{
    public class PredictionRequest
    {
        [JsonPropertyName("category")]
        public string Category { get; set; }

        [JsonPropertyName("day_of_week")]
        public string Day_Of_Week { get; set; }
    }
}