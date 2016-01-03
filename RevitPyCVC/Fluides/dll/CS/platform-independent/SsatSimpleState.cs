//------------------------------------------------------------------------------
// <auto-generated />
//
// This file was automatically generated by SWIG (http://www.swig.org).
// Version 3.0.5
//
// Do not make changes to this file unless you know what you are doing--modify
// the SWIG interface file instead.
//------------------------------------------------------------------------------


public class SsatSimpleState : SS {
  private global::System.Runtime.InteropServices.HandleRef swigCPtr;

  internal SsatSimpleState(global::System.IntPtr cPtr, bool cMemoryOwn) : base(CoolPropPINVOKE.SsatSimpleState_SWIGUpcast(cPtr), cMemoryOwn) {
    swigCPtr = new global::System.Runtime.InteropServices.HandleRef(this, cPtr);
  }

  internal static global::System.Runtime.InteropServices.HandleRef getCPtr(SsatSimpleState obj) {
    return (obj == null) ? new global::System.Runtime.InteropServices.HandleRef(null, global::System.IntPtr.Zero) : obj.swigCPtr;
  }

  ~SsatSimpleState() {
    Dispose();
  }

  public override void Dispose() {
    lock(this) {
      if (swigCPtr.Handle != global::System.IntPtr.Zero) {
        if (swigCMemOwn) {
          swigCMemOwn = false;
          CoolPropPINVOKE.delete_SsatSimpleState(swigCPtr);
        }
        swigCPtr = new global::System.Runtime.InteropServices.HandleRef(null, global::System.IntPtr.Zero);
      }
      global::System.GC.SuppressFinalize(this);
      base.Dispose();
    }
  }

  public SsatSimpleState.SsatSimpleStateEnum exists {
    set {
      CoolPropPINVOKE.SsatSimpleState_exists_set(swigCPtr, (int)value);
      if (CoolPropPINVOKE.SWIGPendingException.Pending) throw CoolPropPINVOKE.SWIGPendingException.Retrieve();
    } 
    get {
      SsatSimpleState.SsatSimpleStateEnum ret = (SsatSimpleState.SsatSimpleStateEnum)CoolPropPINVOKE.SsatSimpleState_exists_get(swigCPtr);
      if (CoolPropPINVOKE.SWIGPendingException.Pending) throw CoolPropPINVOKE.SWIGPendingException.Retrieve();
      return ret;
    } 
  }

  public SsatSimpleState() : this(CoolPropPINVOKE.new_SsatSimpleState(), true) {
    if (CoolPropPINVOKE.SWIGPendingException.Pending) throw CoolPropPINVOKE.SWIGPendingException.Retrieve();
  }

  public enum SsatSimpleStateEnum {
    SSAT_MAX_NOT_SET = 0,
    SSAT_MAX_DOESNT_EXIST,
    SSAT_MAX_DOES_EXIST
  }

}
