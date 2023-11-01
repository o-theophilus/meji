<script>
	import { module } from '$lib/store.js';

	import Center from '$lib/center.svelte';
	import SVG from '$lib/svg.svelte';
	import Button from '$lib/button.svelte';

	import Tag from './tag.svelte';
	import Tags from './_tags.svelte';

	export let tags = [];
	let width;
</script>

<svelte:window bind:innerWidth={width} />

{#if tags.length > 0}
	<div id="tag" />
	<Center>
		<section class="card">
			<div class="ctitle">Tags</div>

			<div class="item_area">
				{#each tags.slice(0, width < 1000 ? 6 : 8) as tag}
					<Tag {tag} />
				{/each}
			</div>
			<br />
			<Button
				class="wide"
				on:click={() => {
					$module = {
						module: Tags,
						tags
					};
				}}
			>
				view all

				<span class="rotate">
					<SVG type="angle" size="10" />
				</span>
			</Button>
		</section>
	</Center>
{/if}

<style>
	.card {
		width: 100%;
		margin-top: var(--sp2);
		border-radius: var(--sp0);

		color: var(--ac2);
		background-color: var(--ac6);
		box-shadow: var(--shad1);
	}
	.ctitle {
		padding: var(--sp3);
	}
	.item_area {
		padding: 0 var(--sp3);
	}

	@media screen and (min-width: 700px) {
		.ctitle {
			padding: var(--sp5);
		}
		.item_area {
			padding: 0 var(--sp5);
		}
	}

	.rotate {
		transform: rotate(180deg);
	}
</style>
