using System;
using System.Text;

namespace IWKS_5300_Lab2
{
  // Define an interface related to ship status
  public interface IShipStatus
  {
    float getFuel();
    int getTorpedoes();
  }

  // Class SpaceShip announces that it will implement this interface
  public class SpaceShip : IShipStatus
  {
    private float FuelAmt;
    private int Torpedoes;

    // Define a constructor for class SpaceShip
    public SpaceShip(float InitialFuel, int InitialTorpedoes)
    {
      FuelAmt = InitialFuel;
      Torpedoes = InitialTorpedoes;
    }

    // Explicitly implement the first interface member
    public float getFuel()
    {
      return FuelAmt;
    }

    // Explicitly implement the second interface member
    public int getTorpedoes()
    {
      return Torpedoes;
    }
  }

  class Program
  {
    static void Main(string[] args)
    {
      // Declare an instance of a SpaceShip
      SpaceShip ship1 = new SpaceShip(1500.0f, 15);

      // Declare the interface instance shipstats
      IShipStatus shipstats = (IShipStatus)ship1;

      // Print out the ship status by calling the methods from an instance of the interface
      Console.WriteLine("Fuel: {0}", shipstats.getFuel());
      Console.WriteLine("Torpedoes: {0}", shipstats.getTorpedoes());

      // Print out the ship status by calling the methods directly from the class
      Console.WriteLine("Fuel: {0}", ship1.getFuel());
      Console.WriteLine("Torpedoes: {0}", ship1.getTorpedoes());
    }
  }
}
