<script>
	import { app, module, page_state } from '$lib/store.svelte.js';

	import { LinkArrow, Button } from '$lib/button';
	import { Content, Card } from '$lib/layout';
	import { Icon } from '$lib/macro';

	import AllTags from './tags.all.svelte';

	let tags = ['male', 'palm', 'female', 'sandals', 'sneakers', 'nike', 'timberland', 'cover shoe'];
</script>

{#if tags.length > 0}
	<div class="page_title" id="tag">Categories</div>
	<LinkArrow onclick={() => module.open(AllTags)} --link-font-size="0.8rem">See All</LinkArrow>

	<div class="block">
		{#each app.tags as tag}
			<button onclick={() => page_state.goto('shop', { tag })}>
				<div class="icon">
					<!-- <Icon icon="logo"></Icon> -->
					{tag}
				</div>
				<!-- {tag} -->
			</button>
		{/each}
	</div>
{/if}

<style>
	.block {
		display: grid;
		grid-template-columns: repeat(4, auto);
		gap: 0 8px;
		grid-template-rows: auto;
		grid-auto-rows: 0;
		overflow: hidden;

		margin-top: 16px;
	}

	@media screen and (min-width: 600px) {
		.block {
			grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
		}
	}

	button {
		all: unset;
		cursor: pointer;

		display: flex;
		flex-direction: column;
		gap: 8px;
		flex-shrink: 0;
		
		text-align: center;
		line-height: 120%;
		
		font-size: 0.8rem;
		text-transform: capitalize;
		
		overflow: hidden;
		
		&:hover .icon {
			background-color: var(--bg2);
		}
	}
	
	.icon {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 8px;
		
		background-color: var(--bg3);
		
		padding: 8px;
		width: 100%;
		aspect-ratio: 1;
		border-radius: 40%;
		line-height: 120%;

		transition: background-color 0.2s ease-in-out;
	}
</style>
