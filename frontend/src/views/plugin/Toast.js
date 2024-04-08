import Swal from "sweetalert2";

/**
 * Creates a Toast instance with predefined settings using SweetAlert2.
 *
 * @returns {Swal} A Swal object configured to display as a toast notification.
 */
function Toast() {
  const Toast = Swal.mixin({
    toast: true,
    position: "top",
    showConfirmButton: false,
    timer: 1500,
    timerProgressBar: true,
  });

  return Toast;
}

export default Toast;
