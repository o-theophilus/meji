<script>
	import { goto } from '$app/navigation';

	// export let size = false;
	export let ads;

	let index = 0;

	// const auto_scroll = () => {
	// 	index += 1;
	// 	if (index > ads.length - 1) {
	// 		index = 0;
	// 	}
	// };

	// let timer = setInterval(auto_scroll, 1000 * 5);
	// const reset_timer = () => {
	// 	clearInterval(timer);
	// 	timer = setInterval(auto_scroll, 1000 * 5);
	// };
</script>

{#if ads.length > 0}
	<section>
		{#each ads as ad}
			<img
				class="x300x300"
				src={ad.ads['300x300']}
				alt={ad.name}
				on:click={() => {
					goto(`/${ads[index].alias}`);
				}}
			/>
		{/each}
	</section>
{/if}

<style>
	section {
		display: flex;
		position: relative;
		box-shadow: var(--shad1);
		border-radius: var(--brad1);
		/* overflow: hidden; */
		overflow: scroll;
		scroll-snap-type: x mandatory;
		scroll-padding: 0 100px;
	}

	img {
		width: 100%;
		cursor: pointer;
		scroll-snap-align: start;
	}
</style>
