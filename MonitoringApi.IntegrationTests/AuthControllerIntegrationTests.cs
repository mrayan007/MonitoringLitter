using Microsoft.VisualStudio.TestTools.UnitTesting;
using System.Net.Http;
using System.Threading.Tasks;
using MonitoringApi;
using Newtonsoft.Json;
using System.Text;
using MonitoringApi.DTOs;

namespace MonitoringApi.IntegrationTests
{
    [TestClass]
    public class AuthControllerIntegrationTests
    {
        private static CustomWebApplicationFactory<Program> _factory;
        private HttpClient _client;

        [ClassInitialize] 
        public static void ClassInitialize(TestContext context)
        {
            _factory = new CustomWebApplicationFactory<Program>();
        }

        [TestInitialize]
        public void TestInitialize()
        {
            _client = _factory.CreateClient();
        }

        [TestMethod]
        public async Task Login_ValidCredentials_ReturnsOkWithToken()
        {
            var loginRequest = new AuthRequestDto
            {
                Username = "admin",
                Password = "password123"
            };
            var content = new StringContent(JsonConvert.SerializeObject(loginRequest), Encoding.UTF8, "application/json");

            var response = await _client.PostAsync("/api/Auth/login", content);

            response.EnsureSuccessStatusCode(); 
            var responseString = await response.Content.ReadAsStringAsync();
            var responseDto = JsonConvert.DeserializeObject<AuthTokenResponseDto>(responseString);

            Assert.IsNotNull(responseDto);
            Assert.IsFalse(string.IsNullOrEmpty(responseDto.AccessToken));
            Assert.IsNotNull(responseDto.ExpiresAt);
        }

        [TestMethod]
        public async Task Login_InvalidCredentials_ReturnsUnauthorized()
        {
            var loginRequest = new AuthRequestDto
            {
                Username = "wronguser",
                Password = "wrongpassword"
            };
            var content = new StringContent(JsonConvert.SerializeObject(loginRequest), Encoding.UTF8, "application/json");

            var response = await _client.PostAsync("/api/Auth/login", content);

            Assert.AreEqual(System.Net.HttpStatusCode.Unauthorized, response.StatusCode);
        }

        [ClassCleanup]
        public static void ClassCleanup()
        {
            _factory.Dispose();
        }
    }
}