using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// this is the script responsible for taking a screenshot and saving it

public class ScreenshotHandler : MonoBehaviour
{

  private Camera myCamera;

  private static ScreenshotHandler instance;

  private bool takeScreenshotOnNextFrame;

  private string screenshot_name;

  private void Awake()
  {
        instance = this;
        myCamera = gameObject.GetComponent<Camera>();
  }


  public static void TakeScreenshot_Static(int width, int height, string _screenshot_name){

    instance.screenshot_name = _screenshot_name;
    instance.myCamera.targetTexture = RenderTexture.GetTemporary(width, height, 16);

    RenderTexture renderTexture = instance.myCamera.targetTexture;

    Texture2D renderResult = new Texture2D(renderTexture.width, renderTexture.height, TextureFormat.ARGB32 , false);

    Rect rect = new Rect(0, 0, renderTexture.width, renderTexture.height);
    renderResult.ReadPixels(rect, 0, 0);

    byte[] byteArray = renderResult.EncodeToPNG();
    System.IO.File.WriteAllBytes(Application.dataPath + "/Screenshots/" + instance.screenshot_name + ".png", byteArray);

    RenderTexture.ReleaseTemporary(renderTexture);
    instance.myCamera.targetTexture = null;

  }

}
