<script>
	import { Button } from '$lib/button';
	import { onMount } from 'svelte';

	let {
		value = $bindable(),
		disabled = false,
		min = 0,
		max = undefined,
		step = 1,
		ondone
	} = $props();

	let ready = false;

	const set = (val) => {
		if (val === 'increase' || val === 'decrease') {
			const num = Number(value) || 0;
			value = val === 'increase' ? num + step : num - step;
		} else {
			if (val === '') {
				value = '';
				if (ready) ondone?.(value);
				return;
			}

			const num = Number(val);
			value = Number.isNaN(num) ? 0 : num;
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
		type="text"
		inputmode="numeric"
		pattern="[0-9]*"
		{disabled}
		{value}
		oninput={(e) => set(e.target.value)}
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
				'ArrowUp',
				'ArrowDown',
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

			if (e.ctrlKey || e.metaKey) return;

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

			if (!allowedKeys.includes(e.key)) {
				e.preventDefault();
			}
		}}
		onpaste={(e) => {
			e.preventDefault();
			let data = (e.clipboardData || window.clipboardData).getData('text');
			data = data.replace(/\D/g, '');

			const num = parseInt(data);
			set(Number.isNaN(num) ? '' : num);
		}}
		onblur={() => {
			if (value === '') set(min ?? 0);
			else set(value);
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

	form {
		line-height: 0;
	}
</style>
