<script>
	import { state } from '$lib/store.js';

	import Center from '$lib/center.svelte';
	import { onMount } from 'svelte';
	import Control from './control.svelte';

	export let space;
	export let size = '';
	export let placeholder;
	let adverts = [];
	let sizes = ['300x300', '300x600', '600x300', '900x300'];
	$: if (!sizes.includes(size)) {
		size = '';
	}
	let index = 0;
	let width = 0;
	$: left = index * width;

	onMount(async () => {
		let i = $state.findIndex((x) => x.name == space);
		if (i == -1) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/advert_display?status=${space}`);
			resp = await resp.json();
			if (resp.status == 200) {
				adverts = resp.adverts;
				$state.push({
					name: space,
					data: resp.adverts,
					loaded: true
				});
			}
		} else if ($state[i].loaded) {
			adverts = $state[i].data;
		}
	});
</script>

{#if adverts.length == 0 && placeholder}
	<Center>
		<section>
			<div class="ads" bind:offsetWidth={width}>
				{#if size == ''}
					<img class="i300" src="/image/ads_300x300.png" alt="loading" style:width="{width}px" />
					<img class="i600" src="/image/ads_600x300.png" alt="loading" style:width="{width}px" />
					<img class="i900" src="/image/ads_900x300.png" alt="loading" style:width="{width}px" />
				{:else}
					<img src="/image/ads_{size}.png" alt="loading" style:width="{width}px" />
				{/if}
			</div>
		</section>
	</Center>
{:else}
	<Center>
		<section>
			<div class="ads" bind:offsetWidth={width}>
				<div class="scroller" style:left="-{left}px">
					{#each adverts as x}
						<a href="/{x.slug}">
							{#if size == ''}
								<img class="i300" src={x[`photo_300x300`]} alt={x.name} style:width="{width}px" />
								<img class="i600" src={x[`photo_600x300`]} alt={x.name} style:width="{width}px" />
								<img class="i900" src={x[`photo_900x300`]} alt={x.name} style:width="{width}px" />
							{:else}
								<img src={x[`photo_${size}`]} alt={x.name} style:width="{width}px" />
							{/if}
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

		overflow: hidden;
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

	.i600 {
		display: none;
	}
	.i900 {
		display: none;
	}
	@media screen and (min-width: 600px) {
		.i300 {
			display: none;
		}
		.i600 {
			display: unset;
		}
		.i900 {
			display: none;
		}
	}
	@media screen and (min-width: 900px) {
		.i300 {
			display: none;
		}
		.i600 {
			display: none;
		}
		.i900 {
			display: unset;
		}
	}
</style>
