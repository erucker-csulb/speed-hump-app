using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using ArcGIS.Core.CIM;
using ArcGIS.Core.Data;
using ArcGIS.Core.Geometry;
using ArcGIS.Desktop.Catalog;
using ArcGIS.Desktop.Core;
using ArcGIS.Desktop.Editing;
using ArcGIS.Desktop.Extensions;
using ArcGIS.Desktop.Framework;
using ArcGIS.Desktop.Framework.Contracts;
using ArcGIS.Desktop.Framework.Dialogs;
using ArcGIS.Desktop.Framework.Threading.Tasks;
using ArcGIS.Desktop.Mapping;

namespace EquationButtons
{
    internal class RunEq_AccHist : Button
    {
        protected override void OnClick()
        {
            QueuedTask.Run(() =>
            {
                try
                {
                    // Inform user that add-in is about to call Python script.
                    ArcGIS.Desktop.Framework.Dialogs.MessageBox.Show("Click OK to start script, and wait for completion messagebox.", "Info");
                    // Create and format path to Pro
                    var pathProExe = System.IO.Path.GetDirectoryName((new System.Uri(Assembly.GetEntryAssembly().CodeBase)).AbsolutePath);
                    if (pathProExe == null) return;
                    pathProExe = Uri.UnescapeDataString(pathProExe);
                    pathProExe = System.IO.Path.Combine(pathProExe, @"Python\envs\arcgispro-py3");
                    // Create and format path to Python
                    var pathPython = System.IO.Path.GetDirectoryName((new System.Uri(Assembly.GetExecutingAssembly().CodeBase)).AbsolutePath);
                    if (pathPython == null) return;
                    pathPython = Uri.UnescapeDataString(pathPython);
                    // Create and format process command string.
                    var myCommand = string.Format(@"/c """"{0}"" ""{1}""""",
                        System.IO.Path.Combine(pathProExe, "python.exe"),
                        System.IO.Path.Combine(pathPython, @"D:\CSULB\SpeedHumps\speed-hump-app\accident_history_eq.py"));
                    // Create process start info, with instruction settings
                    var procStartInfo = new System.Diagnostics.ProcessStartInfo("cmd", myCommand);
                    procStartInfo.RedirectStandardOutput = true;
                    procStartInfo.RedirectStandardError = true;
                    procStartInfo.UseShellExecute = false;
                    procStartInfo.CreateNoWindow = true;
                    // Create process and start it
                    System.Diagnostics.Process proc = new System.Diagnostics.Process();
                    proc.StartInfo = procStartInfo;
                    proc.Start();
                    // Create and format result string
                    string result = proc.StandardOutput.ReadToEnd();
                    string error = proc.StandardError.ReadToEnd();
                    if (!string.IsNullOrEmpty(error)) result += string.Format("{0} Error: {1}", result, error);
                    // Show result string
                    ArcGIS.Desktop.Framework.Dialogs.MessageBox.Show(result, "Info");
                }

                catch (Exception exc)
                {
                    // Catch any exception found and display in a message box
                    ArcGIS.Desktop.Framework.Dialogs.MessageBox.Show("Exception caught while trying to run Python tool: " + exc.Message);
                    return;
                }
            });
        }
    }
}
