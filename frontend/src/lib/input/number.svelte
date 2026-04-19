<script>
	import { Icon } from '$lib/macro';
	import { onMount } from 'svelte';
	let { value = $bindable(), disabled, ondone, icon } = $props();

	let ready = false;
	const round = (num, dp = 2) => Math.round((num + Number.EPSILON) * 10 ** dp) / 10 ** dp;

	const set = (val) => {
		const num = Number(val);
		value = Number.isNaN(num) ? 0 : num;
		value = round(Number(value), 2);
		if (ready) ondone?.(value);
	};

	onMount(() => {
		set(value);
		ready = true;
	});
</script>

<div class="input" class:disabled>
	{#if icon}
		<div class="icon">
			<Icon {icon}></Icon>
		</div>
	{/if}
	<input
		type="number"
		min="0"
		bind:value
		{disabled}
		onkeydown={(e) => {
			if (['-', 'e'].includes(e.key.toLowerCase())) {
				e.preventDefault();
				return;
			}
		}}
		onpaste={(e) => {
			e.preventDefault();
			let data = (e.clipboardData || window.clipboardData).getData('text');
			data = data.replace(/[^0-9.]/g, '');

			const parts = data.split('.');
			if (parts.length > 2) {
				data = parts[0] + '.' + parts.slice(1).join('');
			}

			set(data);
		}}
		onblur={() => {
			set(value);
		}}
	/>
</div>

<style>
	.input {
		display: flex;
		align-items: center;
		width: 100%;
	}

	input {
		width: 100%;
		height: var(--input-height, 56px);
		border: none;
		padding: 0 var(--input-padding-x, 16px);

		background-color: transparent;
		color: var(--ft1);
	}

	input[type='number']::-webkit-outer-spin-button,
	input[type='number']::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}

	.icon {
		line-height: 0;
		padding-left: 16px;
		flex-shrink: 0;
	}
</style>
