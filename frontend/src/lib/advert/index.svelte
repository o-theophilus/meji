<script>
	import Center from '$lib/center.svelte';
	import Control from './control.svelte';

	export let adverts = [];
	export let size = '';
	let sizes = ['300x300', '300x600', '600x300', '900x300'];
	let use_size = sizes[0];
	let index = 0;
	let width = 0;

	$: if (sizes.includes(size)) {
		use_size = size;
	} else if (width < 600) {
		use_size = '300x300';
	} else if (width > 900) {
		use_size = '900x300';
	} else {
		use_size = '600x300';
	}

	$: left = index * width;
</script>

{#if adverts.length > 0}
	<Center>
		<section>
			<div class="ads" bind:offsetWidth={width}>
				<div class="scroller" style:left="-{left}px">
					{#each adverts as x}
						<a href="/{x.slug}">
							<img src={x[`photo_${use_size}`]} alt={x.name} style:width="{width}px" />
						</a>
					{/each}
				</div>
			</div>

			<div class="control">
				<Control
					count={adverts.length}
					on:ok={(e) => {
						index = e.detail;
					}}
				/>
			</div>
		</section>
	</Center>
{/if}

<style>
	section {
		position: relative;

		display: flex;
		justify-content: center;
	}

	.control {
		position: absolute;
		bottom: 0;
	}

	.ads {
		position: relative;

		border-radius: var(--sp0);
		box-shadow: var(--shad1);
		overflow: hidden;

		width: 100%;
	}

	.scroller {
		display: flex;
		position: relative;

		transition-property: left;
		transition-duration: 0ms;
		transition-timing-function: ease-in-out;
	}

	a {
		line-height: 0;
	}
</style>
