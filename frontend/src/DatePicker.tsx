// @ts-nocheck
import { onMount } from "solid-js";
import "cally";

interface CallyDatePickerProps {
  onDateChange?: (date: string) => void;
  buttonText?: string;
}

const CallyDatePicker = (props: CallyDatePickerProps) => {
  let buttonRef: HTMLButtonElement | undefined;
  let calendarRef: HTMLElement | undefined;

  onMount(() => {
    // 组件挂载后设置事件监听
    if (calendarRef) {
      calendarRef.addEventListener("change", (event: Event) => {
        const target = event.target as any;
        const selectedValue = target.value;

        // 更新按钮文本
        if (buttonRef) {
          buttonRef.innerText = selectedValue;
        }

        // 调用回调函数
        props.onDateChange?.(selectedValue);
      });
    }
  });

  return (
    <div class="flex justify-center">
      <button
        ref={buttonRef}
        popoverTarget="cally-popover1"
        class="input input-border"
        id="cally1"
        style="anchor-name:--cally1"
      >
        {props.buttonText || "Pick a date"}
      </button>

      <div
        popover
        id="cally-popover1"
        class="dropdown bg-base-100 rounded-box shadow-lg"
        style="position-anchor:--cally1"
      >
        <calendar-date ref={calendarRef} class="cally">
          <svg
            aria-label="Previous"
            class="fill-current size-4"
            slot="previous"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
          >
            <path fill="currentColor" d="M15.75 19.5 8.25 12l7.5-7.5"></path>
          </svg>
          <svg
            aria-label="Next"
            class="fill-current size-4"
            slot="next"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
          >
            <path fill="currentColor" d="m8.25 4.5 7.5 7.5-7.5 7.5"></path>
          </svg>
          <calendar-month></calendar-month>
        </calendar-date>
      </div>
    </div>
  );
};

export default CallyDatePicker;
