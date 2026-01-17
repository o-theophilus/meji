<script>
	import { module, page_state } from '$lib/store.svelte.js';

	import { Link, Button } from '$lib/button';
	import { Content, Card } from '$lib/layout';
	import { Icon } from '$lib/macro';

	import AllTags from './tags.all.svelte';

	let width = $state();
	let tags = ['male', 'palm', 'female', 'sandals', 'sneakers', 'nike', 'timberland', 'cover shoe'];
</script>

<svelte:window bind:innerWidth={width} />

{#if tags.length > 0}
	<Content --content-height="100%" --content-background-color="var(--bg2)">
		<div id="tag"></div>
		<Card>
			Tags
			<Link onclick={() => module.open(AllTags, { tags })}>view more</Link>
			<br />
			<br />

			<div class="grid">
				{#each tags.slice(0, width < 1000 ? 6 : 8) as tag}
					<Button
						--button-width="100%"
						--button-height="80px"
						onclick={() => page_state.goto('shop', { tag })}
					>
						<div class="a">
							<Icon icon="heart"></Icon>
							{tag}
						</div>
					</Button>
				{/each}
			</div>
		</Card>
	</Content>
{/if}

<style>
	.grid {
		display: grid;
		grid-template-columns: auto auto auto;
		gap: 4px;
	}

	.a {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 4px;
	}
</style>
