package S03_I1_PVBattery "Session 3, I3.1: simplified PV and battery blocks (starting file)"
  extends Modelica.Icons.Package;

  block SimplePV "PV power proportional to irradiance"
    parameter Modelica.Units.SI.Area A = 15 "Panel area";
    parameter Real fAct(unit="1") = 0.9 "Fraction of the area covered by active cells";
    parameter Modelica.Units.SI.Efficiency eta = 0.12 "Conversion efficiency";
    // TODO 1: declare the input G (irradiance on the panel, W/m2) and the output P (W)
    //         with Modelica.Blocks.Interfaces.RealInput / RealOutput.
  equation
    // TODO 2: P from G.
  end SimplePV;

  block SimpleBattery "Battery state of charge with charge and discharge efficiencies, no limits"
    parameter Modelica.Units.SI.Energy EMax(displayUnit="kWh") = 5*3.6e6 "Capacity";
    parameter Modelica.Units.SI.Efficiency etaCha = 0.9 "Efficiency during charging";
    parameter Modelica.Units.SI.Efficiency etaDis = 0.9 "Efficiency during discharging";
    parameter Real SOC_start(unit="1") = 0.5 "Initial state of charge";
    Modelica.Blocks.Interfaces.RealInput P(unit="W")
      "Power sent to the battery (> 0 charging, < 0 discharging)"
      annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
    // TODO 3: declare the output SOC.
  initial equation
    // TODO 4: initial state of charge.
  equation
    // TODO 5: the energy balance of the battery (use an if-expression for the two efficiencies).
  end SimpleBattery;

  model Example "One day (15 April, Turin typical year): PV, constant load, battery takes the difference"
    extends Modelica.Icons.Example;
    Modelica.Blocks.Sources.CombiTimeTable irradiance(
      table=[0,0; 3600,0; 7200,0; 10800,0; 14400,0; 18000,19; 21600,208; 25200,396; 28800,577;
      32400,722; 36000,513; 39600,380; 43200,308; 46800,382; 50400,619; 54000,301; 57600,210;
      61200,135; 64800,0; 68400,0; 72000,0; 75600,0; 79200,0; 82800,0; 86400,0],
      smoothness=Modelica.Blocks.Types.Smoothness.LinearSegments)
      "Global horizontal irradiance [W/m2], hourly, time in s from 00:00 UTC"
      annotation (Placement(transformation(extent={{-90,20},{-70,40}})));
    SimplePV pv annotation (Placement(transformation(extent={{-50,20},{-30,40}})));
    Modelica.Blocks.Sources.Constant load(k=300) "Electrical load [W]"
      annotation (Placement(transformation(extent={{-50,-20},{-30,0}})));
    Modelica.Blocks.Math.Feedback surplus "PV power minus load"
      annotation (Placement(transformation(extent={{-10,20},{10,40}})));
    SimpleBattery battery annotation (Placement(transformation(extent={{30,20},{50,40}})));
    Modelica.Units.SI.Energy E_pv(start=0, fixed=true, displayUnit="kWh") "PV energy";
    Modelica.Units.SI.Energy E_load(start=0, fixed=true, displayUnit="kWh") "Load energy";
    Modelica.Units.SI.Energy E_bat(displayUnit="kWh") = battery.EMax*(battery.SOC - battery.SOC_start)
      "Change of stored energy";
    Modelica.Units.SI.Energy E_loss(displayUnit="kWh") = E_pv - E_load - E_bat
      "Battery losses: energy sent to the battery minus energy stored";
  equation
    der(E_pv) = pv.P;
    der(E_load) = load.y;
    // TODO 6: connect irradiance.y[1] -> pv.G, pv.P and load.y -> surplus, surplus.y -> battery.P.
    annotation (experiment(StopTime=86400, Interval=300, Tolerance=1e-8));
  end Example;
end S03_I1_PVBattery;
