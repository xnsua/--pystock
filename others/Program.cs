using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace luarsolarconverter
{
    class Program
    {
        static void Main(string[] args)
        {
            var lc = new ChineseLunisolarCalendar();
            DateTime tdt = new DateTime(1990,1,1);
            StringBuilder builder = new StringBuilder();
            for (int i = 0; i < 365* 40; ++i)
            {
                tdt = tdt.AddDays(1);
                //Console.WriteLine("-----------------------------------------");
                //Console.WriteLine("Solor::  Year:{0}, Month:{1}, Day:{2}", tdt.Year, tdt.Month, tdt.Day);
                //Console.WriteLine("Lunar::  Year:{0}, Month:{1}, Day:{2}, LeapMonth:{3}", lc.GetYear(tdt),
                //    lc.GetMonth(tdt), lc.GetDayOfMonth(tdt), lc.GetLeapMonth(tdt.Year));
                builder.AppendFormat("{0}-{1}-{2}", tdt.Year, tdt.Month, tdt.Day);
                builder.Append(" ");
                builder.AppendFormat("{0}-{1}-{2}-{3}",lc.GetYear(tdt),
                    lc.GetMonth(tdt), lc.GetDayOfMonth(tdt), lc.GetLeapMonth(tdt.Year ));
                builder.Append("\n");
            }
            System.IO.File.WriteAllText("jqt.test", builder.ToString());
        }
    }
}
