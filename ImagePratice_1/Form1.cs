using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ImagePratice_1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void splitContainer1_Panel2_Paint(object sender, PaintEventArgs e)
        {

        }

        private void splitContainer1_Panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog1 = new OpenFileDialog();
            openFileDialog1.InitialDirectory = "C:\\Users\\BrianLiu\\Documents\\Visual Studio 2013\\Projects\\ImagePratice_1\\src\\";

            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                ImageForm MyImage = new ImageForm(openFileDialog1.FileName);
                MyImage.Show();
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog1 = new OpenFileDialog();
            openFileDialog1.InitialDirectory = "C:\\Users\\BrianLiu\\Documents\\Visual Studio 2013\\Projects\\ImagePratice_1\\src\\";

            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                ImageForm MyImage = new ImageForm(openFileDialog1.FileName);
                MyImage.Show();
                MyImage.doGray(MyImage.getRGBData_unsafe());
            }     
        }

        private void button3_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog1 = new OpenFileDialog();
            openFileDialog1.InitialDirectory="C:\\Users\\BrianLiu\\Documents\\Visual Studio 2013\\Projects\\ImagePratice_1\\src\\";

            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                ImageForm MyImage = new ImageForm(openFileDialog1.FileName);
                MyImage.Show();
                MyImage.doNegative(MyImage.getRGBData_unsafe());
            }
        }

        private void button4_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog1 = new OpenFileDialog();
            openFileDialog1.InitialDirectory = "C:\\Users\\BrianLiu\\Documents\\Visual Studio 2013\\Projects\\ImagePratice_1\\src\\";

            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                ImageForm MyImage = new ImageForm(openFileDialog1.FileName);
                MyImage.Show();
                MyImage.doPowerlaw(MyImage.getRGBData_unsafe());
            }
        }
                
        private void button5_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog1 = new OpenFileDialog();
            openFileDialog1.InitialDirectory = "C:\\Users\\BrianLiu\\Documents\\Visual Studio 2013\\Projects\\ImagePratice_1\\src\\";

            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                ImageForm MyImage = new ImageForm(openFileDialog1.FileName);
                MyImage.Show();
                MyImage.doBinaryThresholding(MyImage.getRGBData_unsafe());
            }
        }

        private void button6_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog1 = new OpenFileDialog();
            openFileDialog1.InitialDirectory = "C:\\Users\\BrianLiu\\Documents\\Visual Studio 2013\\Projects\\ImagePratice_1\\src\\";

            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                ImageForm MyImage = new ImageForm(openFileDialog1.FileName);
                MyImage.Show();
                MyImage.doHistogramEqualization(MyImage.getRGBData_unsafe());
            }
        }
                
        private void button8_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog1 = new OpenFileDialog();
            openFileDialog1.InitialDirectory = "C:\\Users\\BrianLiu\\Documents\\Visual Studio 2013\\Projects\\ImagePratice_1\\src\\";

            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                ImageForm MyImage = new ImageForm(openFileDialog1.FileName);
                MyImage.Show();
                MyImage.doMedianFilter(MyImage.getRGBData_unsafe());
            }
        }

        private void button9_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog1 = new OpenFileDialog();
            openFileDialog1.InitialDirectory = "C:\\Users\\BrianLiu\\Documents\\Visual Studio 2013\\Projects\\ImagePratice_1\\src\\";

            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                ImageForm MyImage = new ImageForm(openFileDialog1.FileName);
                MyImage.Show();
                MyImage.doKmeans(MyImage.getRGBData_unsafe(), 3);
            }
        }
    }

    //顯示圖片的Form類別(新視窗)
    class ImageForm : Form
    {
        Image image;

        //建構子
        public ImageForm(String Filename)
        {
            //載入圖檔
            image = Image.FromFile(Filename);
            this.Text = Filename;
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            //顯示影像
            this.Height = image.Height;
            this.Width = image.Width;

            //顯示出影像
            e.Graphics.DrawImage(image, 0, 0, Width, Height);
        }

       //傳回RGB陣列資訊
        /*public int[,,] getRGBData()
        {
            Bitmap bimage = new Bitmap(image);
            int Height = bimage.Height;
            int Width = bimage.Width;
            int[, ,] rgbData = new int[Width, Height, 3];

            for (int y = 0; y < Height; y++) 
            {
                for (int x = 0; x < Width; x++) 
                {
                    Color color = bimage.GetPixel(x, y);
                    rgbData[x, y, 0] = color.R;
                    rgbData[x, y, 1] = color.G;
                    rgbData[x, y, 2] = color.B;
                }
            }
            return rgbData;
        }*/

        //傳回RGB陣列資訊-使用指標
        public int[, ,] getRGBData_unsafe()
        {
            Bitmap bimage = new Bitmap(image);
            return getRGBData(bimage);
        }

        public static int[, ,] getRGBData(Bitmap bimage)
        {
            //鎖住存放圖片的記憶體
            BitmapData bmData = bimage.LockBits(new Rectangle(0, 0, bimage.Width, bimage.Height), ImageLockMode.ReadOnly, PixelFormat.Format24bppRgb);
            int stride = bmData.Stride;
            //取得像點資料的起始位置
            System.IntPtr Scan0 = bmData.Scan0;
            //計算每行像點所佔據的Byte總數
            int ByteNumber_Width = bimage.Width * 3;
            //計算每一行後面幾個Paddind bytes
            int ByteOfSkip = stride - ByteNumber_Width;
            int Height = bimage.Height;
            int Width = bimage.Width;
            int[, ,] rgbData = new int[Width, Height, 3];

            //直接利用指標，將影像資料取出來 BGR
            unsafe
            {
                byte* p = (byte*)(void*)Scan0;
                for (int y = 0; y < Height; y++)
                {
                    for (int x = 0; x < Width; x++)
                    {
                        rgbData[x, y, 2] = p[0];
                        ++p;
                        rgbData[x, y, 1] = p[0];
                        ++p;
                        rgbData[x, y, 0] = p[0];
                        ++p;
                    }
                    p += ByteOfSkip;
                }
            }
            bimage.UnlockBits(bmData);
            return rgbData;
        }

        //設定像素-使用指標
        public void setRGBData_unsafe(int[, ,] rgbData)
        {
            Bitmap bimage = CreateBitmap(rgbData);
            image = bimage;
            this.Refresh();
        }
        public static Bitmap CreateBitmap(int[, ,] rgbData)
        {
            int Width = rgbData.GetLength(0);
            int Height = rgbData.GetLength(1);

            Bitmap bimage = new Bitmap(Width, Height, PixelFormat.Format24bppRgb);

            // Step 1: 先鎖住存放圖片的記憶體
            BitmapData bmData = bimage.LockBits(new Rectangle(0, 0, Width, Height),
                                           ImageLockMode.WriteOnly,
                                           PixelFormat.Format24bppRgb);
            int stride = bmData.Stride;

            // Step 2: 取得像點資料的起始位址
            System.IntPtr Scan0 = bmData.Scan0;

            // 計算每行的像點所佔據的byte 總數
            int ByteNumber_Width = bimage.Width * 3;

            // 計算每一行後面幾個 Padding bytes
            int ByteOfSkip = stride - ByteNumber_Width;


            // Step 3: 直接利用指標, 把影像資料取出來
            unsafe
            {
                byte* p = (byte*)(void*)Scan0;
                for (int y = 0; y < Height; y++)
                {
                    for (int x = 0; x < Width; x++)
                    {
                        p[0] = (byte)rgbData[x, y, 2]; // 先放 B
                        ++p;
                        p[0] = (byte)rgbData[x, y, 1];  // 再放 G 
                        ++p;
                        p[0] = (byte)rgbData[x, y, 0];  // 最後放 R  
                        ++p;
                    }
                    p += ByteOfSkip; // 跳過剩下的 Padding bytes
                }
            }

            bimage.UnlockBits(bmData);
            return bimage;
        }

        //灰階平均值法
        public void doGray(int[, ,] rgbData)
        {
            
            Bitmap bimage = new Bitmap(image);
            int Width = bimage.Width;
            int Height = bimage.Height;

            int[,,] newRGBData = new int[Width, Height, 3];
            for (int y = 0; y < Height; y++) {
                for (int x = 0; x < Width; x++)
                {
                    int gray = (rgbData[x, y, 0] + rgbData[x, y, 1] + rgbData[x, y, 2]) / 3;
                    //bimage.SetPixel(x, y, Color.FromArgb(gray, gray, gray));

                    for (int i = 0; i < 3; i++)
                    {
                        newRGBData[x, y, i] = gray;
                    }
                }
            }

            setRGBData_unsafe(newRGBData);

            /*image = bimage;
            this.Refresh();*/
        }

        //負片
        public void doNegative(int[,,] rgbData)
        {
            Bitmap bimage = new Bitmap(image);
            int Width = bimage.Width;
            int Height = bimage.Height;

            int[, ,] newRGBData = new int[Width, Height, 3];
            for (int y = 0; y < Height; y++)
            {
                for (int x = 0; x < Width; x++)
                {
                    //bimage.SetPixel(x, y, Color.FromArgb(255 - rgbData[x, y, 0], 255 - rgbData[x, y, 1], 255 - rgbData[x, y, 2]));

                    for (int i = 0; i < 3; i++)
                    {
                        newRGBData[x, y, i] = 255 - rgbData[x, y, i];
                    }
                }
            }
            setRGBData_unsafe(newRGBData);
            /*image = bimage;
            this.Refresh();*/
        }

        //Power –law
        public void doPowerlaw(int[, ,] rgbData)
        {
            Bitmap bimage = new Bitmap(image);
            int Width = bimage.Width;
            int Height = bimage.Height;
            int c = 1;
            double r = 0.7;

            int[, ,] newRGBData = new int[Width, Height, 3];
            for (int y = 0; y < Height; y++)
            {
                for (int x = 0; x < Width; x++)
                {
                    //c*x^r,c依照最高的點用來下修到低於255
                    int R = rgbData[x,y,0];
                    int G = rgbData[x, y, 1];
                    int B = rgbData[x, y, 2];
                    /*for(int i=r;i>0;i--)
                    {
                        R = R* R;
                        G = G * G;
                        B = B * B;
                    }*/
                    R = c * (int)(Math.Pow(R, r));                    
                    G = c * (int)(Math.Pow(G, r));                    
                    B = c * (int)(Math.Pow(B, r));
                    /*if (R > 255)
                        R = 255;
                    if (G > 255)
                        G = 255;
                    if (B > 255)
                        B = 255;*/
                    //bimage.SetPixel(x, y, Color.FromArgb(R, G, B));
                    newRGBData[x, y, 0] = R;
                    newRGBData[x, y, 1] = G;
                    newRGBData[x, y, 2] = B;
                }
            }
            setRGBData_unsafe(newRGBData);
            /*image = bimage;
            this.Refresh();*/
        }

        //Binary Thresholding 二值化 平均灰階值法
        public void doBinaryThresholding(int[, ,] rgbData)
        {
            Bitmap bimage = new Bitmap(image);
            int Width = bimage.Width;
            int Height = bimage.Height;            
            int graySum = 0;

            for (int y = 0; y < Height; y++)
            {
                for (int x = 0; x < Width; x++)
                {
                    graySum = graySum + rgbData[x, y, 0];
                }
            }
            int threshold = graySum / (Width * Height);

            int[, ,] newRGBData = new int[Width, Height, 3];
            for (int y = 0; y < Height; y++)
            {
                for (int x = 0; x < Width; x++)
                {
                    if (rgbData[x, y, 0] > threshold)
                    {
                        //bimage.SetPixel(x, y, Color.FromArgb(255, 255, 255));
                        for (int i = 0; i < 3; i++)
                            newRGBData[x, y, i] = 255;
                    }
                    else
                    {
                        //bimage.SetPixel(x, y, Color.FromArgb(0, 0, 0));
                        for (int i = 0; i < 3; i++)
                            newRGBData[x, y, i] = 0;
                    }
                }
            }
            setRGBData_unsafe(newRGBData);
            /*image = bimage;
            this.Refresh();*/
        }

        //Histogram equalization 直方圖
        public void doHistogramEqualization(int[, ,] rgbData)
        {
            Bitmap bimage = new Bitmap(image);
            int Width = bimage.Width;
            int Height = bimage.Height;
            int[,] countList = new int[256, 3];

            //掃描像素點統計RGB值
            for (int y = 0; y < Height; y++)
            {
                for (int x = 0; x < Width; x++)
                {
                    for (int i = 0; i < 3; i++)
                    {
                        countList[rgbData[x, y, i], i]++;
                    }
                }
            }

            int[,] valueList = new int[256, 3];

            //nj/(x*y)*255, 255/x/y
            //double fc = 255 / Width / Height;
            float[] countTmp = new float[3];           

            for (int i = 0; i < 256; i++)
            {                                
                for (int j = 0; j < 3; j++)
                {
                    countTmp[j] = countTmp[j] + countList[i, j];
                    valueList[i, j] = (int)(countTmp[j] / Width / Height * 255);
                }
            }

            //像素點設值
            int[, ,] newRGBData = new int[Width, Height, 3];
            for (int y = 0; y < Height; y++)
            {
                for (int x = 0; x < Width; x++)
                {
                    //bimage.SetPixel(x, y, Color.FromArgb(valueList[rgbData[x, y, 0], 0], valueList[rgbData[x, y, 1], 1], valueList[rgbData[x, y, 2], 2]));
                    for (int i = 0; i < 3; i++)
                        newRGBData[x, y, i] = valueList[rgbData[x, y, i], i];
                }
            }
            setRGBData_unsafe(newRGBData);
            /*image = bimage;
            this.Refresh();*/
        }

        //Median Filter 中值濾波器
        public void doMedianFilter(int[,,] rgbData)
        {
            Bitmap bimage = new Bitmap(image);
            int Width = bimage.Width;
            int Height = bimage.Height;

            int[, ,] newRGBData = new int[Width, Height, 3];
            for (int y = 1; y < Height - 1; y++)
            {
                for (int x = 1; x < Width - 1; x++)
                {
                    //觀察窗3*3設值
                    int[,] window = new int[9, 3];
                    int windowKey = 0;
                    for (int yy = y - 1; yy < y + 2; yy++)
                    {
                        for (int xx = x - 1; xx < x + 2; xx++)
                        {
                            for (int i = 0; i < 3; i++)
                            {
                                window[windowKey, i] = rgbData[xx, yy, i];                                
                            }
                            windowKey++;
                        }
                    }
                    //觀察窗排序
                    //Array.Sort(window);
                    for (int i = 0; i < 5; i++)
                    {
                        int[] min = new int[]{i, i, i};
                        for (int j = i + 1; j < 9; j++)
                        {
                            for(int k=0;k<3;k++)
                                if (window[j,k] < window[min[k],k])
                                    min[k] = j;
                        }
                        for(int j=0;j<3;j++ )
                        {
                            if (i != min[j])
                            {
                                int temp = window[i, j];
                                window[i, j] = window[min[j], j];
                                window[min[j], j] = temp;
                            }
                        }   
                    }
                    //新圖片設值
                    for (int i = 0; i < 3; i++)
                        newRGBData[x, y, i] = window[4, i];
                }
            }
            setRGBData_unsafe(newRGBData);
        }


        public int kmeansCount = 0;
        public void doKmeans(int[, ,] rgbData, int k)
        {
            Bitmap bimage = new Bitmap(image);
            int Width = bimage.Width;
            int Height = bimage.Height;

            //設定 K 與 隨機初始值u(顏色)
            //int[] u = new int[k];
            int[] u = new int[k];
            for (int i = 0; i < k; i++)
            {
                Random rnd = new Random();
                u[i] = rnd.Next(0, 255);
                for (int j = 0; j < i; j++)
                {
                    while (u[j] == u[i])
                    {
                        j = 0;
                        u[i] = rnd.Next(0, 255);
                    }
                }
            }
            

            int[,] group = new int[Width, Height];
            kmeansCount = 0;
            //遞迴->統計、歸類->新群
            //kmeansClustering(rgbData, u, Width, Height);

            KmeansData kmeansdata = new KmeansData(rgbData, u, Width, Height);

            int[, ,] newRGBData = new int[Width, Height, 3];
            for (int y = 0; y < Height; y++)
            {
                for (int x = 0; x < Width; x++)
                {
                    for(int i=0;i<3;i++)
                    {
                        //新圖片設值
                        newRGBData[x, y, i] = kmeansdata.u[kmeansdata.group[x, y]]; //u[group[x,y]]
                    }
                }
            }
            setRGBData_unsafe(newRGBData);
            Console.Write(u[0]+","+u[1]+","+u[2]+"\n");
        }

        public class KmeansData
        {
            private int[, ,]rgbData;
            public int[] u;
            private int Width;
            private int Height;
            public int[,] group;
            private int[,] coSet;

            private int count;

            public KmeansData()
            {
                //空白建構元
                this.rgbData=new int[0, 0, 0];
                this.u = new int[0];
                this.Width = 0;
                this.Height = 0;
                this.group = new int[0, 0];
                this.coSet = new int[0, 0];

                this.count = 0;
            }

            public KmeansData(int[, ,] rgbData, int[] u, int Width, int Height)
            {
                this.count = 0;

                this.rgbData = rgbData;
                this.u = u;
                this.Width = Width;
                this.Height = Height;
                this.group = new int[Width, Height];
                //值集合與群裡點的個數
                this.coSet = new int[u.Length, 2];

                //KmeansData kmeansdata = new KmeansData(this.rgbData, this.u, this.Width, this.Height);
                cluster(this.u);
            }

            private int  cluster(int[] u)
            {
                for (int y = 0; y < Height; y++)
                {
                    for (int x = 0; x < Width; x++)
                    {
                        double minDest = Math.Pow(rgbData[x, y, 0] - u[0], 2);
                        group[x, y] = 0;

                        for (int i = 1; i < u.Length; i++)
                        {
                            if (Math.Pow(rgbData[x, y, 0] - u[i], 2) < minDest)
                            {
                                minDest = Math.Pow(rgbData[x, y, 0] - u[i], 2);
                                group[x, y] = i;
                            }
                        }
                        //累加值
                        coSet[group[x, y], 0] += rgbData[x, y, 0];
                        //計算個數
                        coSet[group[x, y], 1]++;
                    }
                }

                //上一個群中心
                int[] pre_u = new int[u.Length];
                Array.Copy(u, pre_u, u.Length);

                //計算中心
                for (int i = 0; i < u.Length; i++)
                {
                    //待處理問題:有時選的初始點會造成某一群會沒有所屬的點，變成除以0的錯誤
                    u[i] = coSet[i, 0] / coSet[i, 1];
                }

                count++;
                Console.Write(count + "\n");

                //比較新舊群中心
                bool u_equal = true;
                for (int i = 0; i < u.Length; i++)
                {
                    if (u[i] != pre_u[i])
                        u_equal = false;
                }
                int count_u_equal = 0;
                while (u_equal)
                {
                    if (u[count_u_equal] != pre_u[count_u_equal])
                        u_equal = false;

                    count_u_equal++;
                    if (count_u_equal == u.Length)
                        break;
                }

                if (u_equal)
                    return 0;//@@
                return cluster(u);//@@

                /*if(count<5)
                    return cluster(u);

                //需群中心、屬於哪個群
                return 0;*/
            }
        }
    }
}
