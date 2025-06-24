using Microsoft.VisualStudio.TestTools.UnitTesting;
using MonitoringApi.Controllers;
using Microsoft.Extensions.Configuration;
using Moq;
using MonitoringApi.DTOs;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System.Text;
using System.IdentityModel.Tokens.Jwt;

namespace MonitoringApi.UnitTests.Controllers
{
    [TestClass]
    public class AuthControllerTests
    {
        private Mock<IConfiguration> _mockConfiguration;
        private Mock<IConfigurationSection> _mockJwtSection;

        [TestInitialize] 
        public void Setup()
        {
            _mockConfiguration = new Mock<IConfiguration>();
            _mockJwtSection = new Mock<IConfigurationSection>();

            _mockJwtSection.Setup(s => s["Secret"]).Returns("ThisIsAVerySecureSecretKeyForTesting123");
            _mockJwtSection.Setup(s => s["Issuer"]).Returns("TestIssuer");
            _mockJwtSection.Setup(s => s["Audience"]).Returns("TestAudience");
            _mockJwtSection.Setup(s => s["TokenLifetimeMinutes"]).Returns("1");

            _mockConfiguration.Setup(c => c.GetSection("Jwt")).Returns(_mockJwtSection.Object);
        }

        [TestMethod]
        public void Login_ValidCredentials_ReturnsOkWithToken()
        {
            var controller = new AuthController(_mockConfiguration.Object);
            var model = new AuthRequestDto { Username = "admin", Password = "password123" };

            var result = controller.Login(model) as OkObjectResult;

            Assert.IsNotNull(result);
            Assert.AreEqual(200, result.StatusCode);

            var responseDto = result.Value as AuthTokenResponseDto;
            Assert.IsNotNull(responseDto);
            Assert.IsFalse(string.IsNullOrEmpty(responseDto.AccessToken));
            Assert.IsNotNull(responseDto.ExpiresAt);

            var tokenHandler = new JwtSecurityTokenHandler();
            var token = tokenHandler.ReadToken(responseDto.AccessToken) as JwtSecurityToken;
            Assert.IsNotNull(token);
            Assert.AreEqual("TestIssuer", token.Issuer);
            Assert.AreEqual("TestAudience", token.Audiences.First());
            Assert.AreEqual("admin", token.Claims.First(c => c.Type == JwtRegisteredClaimNames.Sub).Value);
        }

        [TestMethod]
        public void Login_InvalidCredentials_ReturnsUnauthorized()
        {
            var controller = new AuthController(_mockConfiguration.Object);
            var model = new AuthRequestDto { Username = "wronguser", Password = "wrongpassword" };

            var result = controller.Login(model) as UnauthorizedObjectResult;

            Assert.IsNotNull(result);
            Assert.AreEqual(401, result.StatusCode);
        }
    }
}