// DiscService.cs

using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace DiscBagProject
{
    public class DiscService
    {
        private readonly HttpClient httpClient;

        public DiscService(string baseAddress)
        {
            httpClient = new HttpClient { BaseAddress = new Uri(baseAddress) };
        }

        public async Task<List<DiscModel>> GetDiscsAsync()
        {
            return await httpClient.GetFromJsonAsync<List<DiscModel>>("/discs/");
        }

        public async Task<DiscModel> GetDiscByNameAsync(string name)
        {
            return await httpClient.GetFromJsonAsync<DiscModel>($"/discs/{name}");
        }

        public async Task<List<DiscModel>> GetDiscsInBagAsync()
        {
            return await httpClient.GetFromJsonAsync<List<DiscModel>>("/inbag");
        }

        public async Task<bool> AddExistingDiscToBagAsync(string discName)
        {
            try
            {
                string encodedDiscName = Uri.EscapeDataString(discName);
                string apiUrl = $"/discs/inbag/{encodedDiscName}";

                HttpResponseMessage response = await httpClient.PostAsync(apiUrl, null);

                if (response.IsSuccessStatusCode)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            catch (Exception ex)
            {
                throw new Exception($"Failed to add disc to bag: {ex.Message}");
            }
        }

        public async Task<bool> RemoveDiscFromBagAsync(string name)
        {
            try
            {
                // Modify the request URL
                var response = await httpClient.DeleteAsync($"/discs/inbag/{name}");
                response.EnsureSuccessStatusCode();
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }

        public async Task<bool> CreateDiscAsync(DiscModel disc)
        {
            try
            {
                // Serialize the disc object to JSON manually
                string jsonDisc = JsonConvert.SerializeObject(disc);
                string apiUrl = $"/discs/";

                // Create a StringContent with the serialized JSON
                StringContent content = new StringContent(jsonDisc, Encoding.UTF8, "application/json");

                // Send the POST request
                HttpResponseMessage response = await httpClient.PostAsJsonAsync(apiUrl, disc);

                // Ensure the request was successful
                response.EnsureSuccessStatusCode();

                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }



        public async Task<bool> UpdateDiscAsync(string name, DiscModel updatedDisc)
        {
            try
            {
                var response = await httpClient.PutAsJsonAsync($"/discs/{name}", updatedDisc);
                response.EnsureSuccessStatusCode();
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }

        public async Task<bool> DeleteDiscAsync(string name)
        {
            try
            {
                var response = await httpClient.DeleteAsync($"/discs/{name}");
                response.EnsureSuccessStatusCode();
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }
    }
}



