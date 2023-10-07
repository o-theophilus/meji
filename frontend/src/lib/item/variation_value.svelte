<script>
	export let active = false;
	export let value;
	export let button = false;
	$: v = value.split(':');

	const style = (bgc) => {
		helper.style.backgroundColor = bgc;
		bgc = window.getComputedStyle(helper).backgroundColor;
		const rgb_array = bgc.match(/\d+/g).map(Number);

		const luminance_color = (rgb_array[0] * 299 + rgb_array[1] * 587 + rgb_array[2] * 114) / 1000;
		const luminance_black = (0 * 299 + 0 * 587 + 0 * 114) / 1000;
		const luminance_white = (255 * 299 + 255 * 587 + 255 * 114) / 1000;
		const contrast1 = Math.abs(luminance_color - luminance_black);
		const contrast2 = Math.abs(luminance_color - luminance_white);

		let color = contrast1 > contrast2 ? 'black' : 'white';
		return color;
	};

	let helper;
</script>

<!-- <span bind:this={helper} /> -->

<button class:active class:button on:click>
	{#if v[0]}
		<div class="name">{v[0]}</div>
	{/if}

	{#if v[0] && v[1]}
		<div class="gap" />
	{/if}

	{#if v[1]}
		<div class="color" style:background-color={v[1]} />
	{/if}
</button>

<style>
	button {
		display: inline-flex;
		align-items: center;

		border: none;

		background-color: transparent;
		border-bottom: 2px solid transparent;
		color: var(--ac2);
	}

	.gap {
		margin-left: var(--sp0);
	}
	.color {
		height: 16px;
		aspect-ratio: 1/1;
		border-radius: 50%;
		border: 2px solid var(--ac3);
	}

	.button {
		cursor: pointer;
	}
	.button:hover {
		border-color: var(--ac4);
	}
	.button.active {
		border-color: var(--cl1);
	}
</style>
