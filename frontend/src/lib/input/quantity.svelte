<script>
	import { Button } from '$lib/button';
	import { onMount } from 'svelte';

	let { value = $bindable(), disabled = false, min = 0, max = null, ondone } = $props();

	let ready = false;

	const set = (val) => {
		let num = Number(val);
		let action = null;
		if (val == 'increase' || val == 'decrease') {
			num = Number(value);
			action = val;
		}

		value = Number.isNaN(num) ? 0 : num;
		if (action) {
			value = action == 'increase' ? value + 1 : value - 1;
		}

		const maxNum = max != null ? Number(max) : null;
		const minNum = min != null ? Number(min) : null;
		if (maxNum != null && value > maxNum) value = maxNum;
		if (minNum != null && value < minNum) value = minNum;

		if (ready) ondone?.(value);
	};

	onMount(() => {
		set(value);
		ready = true;
	});
</script>

<div class="block">
	<form onsubmit={(e) => e.preventDefault()}>
		<Button {disabled} icon="minus" tabindex={-1} onclick={() => set('decrease')} />
	</form>

	<input
		type="number"
		min="0"
		bind:value
		{disabled}
		oninput={(e) => set(e.target.value)}
		onkeydown={(e) => {
			if (['.', '-', 'e'].includes(e.key.toLowerCase())) {
				e.preventDefault();
				return;
			}

			if (e.key === 'ArrowUp') {
				e.preventDefault();
				set('increase');
				return;
			}

			if (e.key === 'ArrowDown') {
				e.preventDefault();
				set('decrease');
				return;
			}
		}}
		onpaste={(e) => {
			e.preventDefault();
			let data = (e.clipboardData || window.clipboardData).getData('text');
			data = data.replace(/\D/g, '');
			set(data);
		}}
		onblur={() => {
			set(value);
		}}
	/>

	<div class="width_helper">
		{value}
	</div>

	<form onsubmit={(e) => e.preventDefault()}>
		<Button {disabled} icon="plus" tabindex={-1} onclick={() => set('increase')} />
	</form>
</div>

<style>
	.block {
		position: relative;

		display: flex;
		align-items: center;
		padding: 2px;

		width: fit-content;

		--button-height: var(--number-height, 44px);
		--button-width: var(--number-width, 44px);
	}

	.width_helper {
		visibility: hidden;
		padding: 0 var(--number-pading-x, 16px);
		min-width: var(--input-min-width, 60px);
	}

	input {
		position: absolute;
		top: 0;
		bottom: 0;
		right: var(--button-width);
		left: var(--button-width);

		border: none;

		font-size: var(--input-font-size, 1rem);
		text-align: center;
		background-color: transparent;
	}
	input[type='number']::-webkit-outer-spin-button,
	input[type='number']::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}

	form {
		line-height: 0;
	}
</style>
