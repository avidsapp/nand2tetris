using System;
using System.Text;

namespace IWKS_5300_Lab2
{
  public abstract class Starship
  {
    // Instance variables
    private double FuelCapacity;
    private double MaxSpeed;
    public int ShieldStrength;
    public bool ShieldsUp = false;

    // Class Methods
    public double GetFuelCapacity()
    {
      return FuelCapacity;
    }
    public double GetMaxSpeed()
    {
      return MaxSpeed;
    }
    public int GetShieldStrength()
    {
      return ShieldStrength;
    }
    public bool GetShieldStatus()
    {
      if(ShieldsUp)
      {
        return true;
      }
      else
      {
        return false;
      }
    }

    // Required instance methods
    public abstract void ReFuel(double amount);
    public abstract void ReArm();
    public abstract void RaiseShields();
  }

  // FastScout instance inheriting Starship
  public class FastScout : Starship
  {
    // Private constant
    private const int FastScoutShieldStrength = 5;

    // Override required instance methods (required by compiler)
    public override void ReFuel(double amount)
    {
      // Increase the fuel load by amount, up to FuelCapacity
    }
    public override void ReArm()
    {
      // Rearm according to what a FastCout can carry
    }
    public override void RaiseShields()
    {
      // Raise the ship's meager shields
      ShieldsUp = true;
      ShieldStrength = FastScoutShieldStrength;
    }

    public void ReportShipsInArea()
    {
      // Scan the are and report (in some way) if there are other ships in the vicinity
    }
  }

  // CargoShip instance inheriting Starship
  public class CargoShip : Starship
  {
    private const int CargoShieldStrength = 3;

    public override void ReFuel(double amount)
    {
      // Increase the fuel load by amount, up to FuelCapacity
    }
    public override void ReArm()
    {
      // Rearm according to what a Cargo Ship can carry
    }
    public override void RaiseShields()
    {
      // Raise the ship's meager Shields
      ShieldsUp = true;
      ShieldStrength = CargoShieldStrength;
    }

    public void LoadCargo()
    {
      // Take on cargo
    }
  }

  class Program
  {
    static void Main(string[] args)
    {
      Starship[] myFleetArray = new Starship[2];

      myFleetArray[0] = new FastScout();
      myFleetArray[1] = new CargoShip();

      foreach (Starship myShip in myFleetArray)
      {
        myShip.ReFuel(15);
        myShip.ReArm();
      }

      // Provide user feedback
      int fleetCount = myFleetArray.Length;
      Console.WriteLine("# of ships = {0}", fleetCount);
    }
  }
}
