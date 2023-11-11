<script>
	import Center from '$lib/center.svelte';
	import Control from './control.svelte';

	export let size = '300x300';
	export let adverts = [];

	let index = 0;
	let width = 0;
	$: left = index * width;

	const auto_scroll = () => {
		index += 1;
		if (index > adverts.length - 1) {
			index = 0;
		}
	};

	let timer = setInterval(auto_scroll, 1000 * 5);
	const reset_timer = () => {
		clearInterval(timer);
		timer = setInterval(auto_scroll, 1000 * 5);
	};
</script>

{#if adverts.length > 0}
	<Center>
		<section bind:offsetWidth={width}>
			<div class="scroller" style:left="-{left}px">
				{#each adverts as ads}
					<a href="/{ads.item.slug}">
						<img src={ads.photos[size]} alt={ads.item.name} style:width="{width}px" />
					</a>
				{/each}
			</div>

			<Control
				{index}
				count={adverts.length}
				on:ok={(e) => {
					index = e.detail;
					reset_timer();
				
				}}
			/>
		</section>
	</Center>
{/if}

<style>
	section {
		position: relative;

		border-radius: var(--sp0);
		box-shadow: var(--shad1);
		overflow: hidden;
	}

	.scroller {
		display: flex;
		position: relative;

		transition-property: left;
		transition-duration: 0s;
		transition-timing-function: ease-in-out;
	}

	a {
		display: flex;
	}
</style>
