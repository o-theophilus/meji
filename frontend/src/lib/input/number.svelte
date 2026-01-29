<script>
	import { Icon } from '$lib/macro';
	import { Button } from '$lib/button';
	let { value = $bindable(), disabled } = $props();

	let width = $state();
</script>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<Button
		icon="minus"
		tabindex={-1}
		onclick={() => {
			value--;
			value = value < 1 ? 1 : value;
		}}
	></Button>
</form>

<input
	style:width="{width}px"
	type="number"
	bind:value
	{disabled}
	onkeydown={(e) => {
		const allowedKeys = [
			'Backspace',
			'Delete',
			'Tab',
			'Escape',
			'Enter',
			'Home',
			'End',
			'ArrowLeft',
			'ArrowRight',
			'0',
			'1',
			'2',
			'3',
			'4',
			'5',
			'6',
			'7',
			'8',
			'9'
		];

		if (e.ctrlKey) {
			return;
		}

		if (!allowedKeys.includes(e.key)) {
			e.preventDefault();
			return;
		}
	}}
	onpaste={(e) => {
		e.preventDefault();
		let data = (e.clipboardData || window.clipboardData).getData('text');
		data = data.replace(/\D/g, '');
		value = parseInt(data);
	}}
/>

<form onsubmit={(e) => e.preventDefault()} novalidate autocomplete="off">
	<Button
		icon="plus"
		tabindex={-1}
		onclick={() => {
			value++;
		}}
	></Button>
</form>

<div class="width_helper" bind:clientWidth={width}>
	{value}
</div>

<style>
	.width_helper {
		position: absolute;
		visibility: hidden;
		padding: 0 16px;
		min-width: 60px;
	}

	input {
		height: var(--input-height, 48px);
		border: none;

		font-size: var(--input-font-size, 1rem);
		text-align: center;
		background-color: var(--input-background-color, transparent);
		color: var(--input-color, hsl(0, 0%, 0%));
	}
	input:not(:last-of-type) {
		border-right: 1px solid var(--input);
	}

	input[type='number']::-webkit-outer-spin-button,
	input[type='number']::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}
</style>
