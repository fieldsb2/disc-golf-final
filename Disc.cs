// DiscModel.cs
namespace DiscBagProject
{
    public class DiscModel
    {
        public string Manufacturer { get; set; } = "";
        public string Name { get; set; } = "";
        public float Speed { get; set; }
        public float Glide { get; set; }
        public float Turn { get; set; }
        public float Fade { get; set; }
        public float Diameter { get; set; }
        public float Height { get; set; }
        public float RimDepth { get; set; }
        public float RimWidth { get; set; }
        public int? Distance { get; set; }
    }
}

