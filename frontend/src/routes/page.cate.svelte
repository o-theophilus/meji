<script>
	import { goto } from '$app/navigation';
	import { state } from '$lib/page_state.js';

	import { module } from '$lib/store.js';
	import Category from './page.cate.form.svelte';

	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body_item.svelte';
	import SVG from '$lib/comp/svg2.svelte';
	import Button from '$lib/comp/button.svelte';

	export let categories = [];
</script>

{#if categories.length > 0}
	<div id="category" />
	<Card>
		<Title title="Categories">
			<Button
				class="tiny link"
				name="view all >"
				on:click={() => {
					$module = {
						module: Category,
						categories
					};
				}}
			/>
		</Title>

		<Body grid>
			{#each categories.slice(0, 6) as category}
				<div
					class="category"
					on:keypress
					on:click={() => {
						$state['shop'].search = '';
						$state['shop'].category = category.name;
						$state['shop'].page_no = 1;
						goto('/shop');
					}}
				>
					<SVG type={category.icon} size="30" />
					<div>
						{category.name}
					</div>
				</div>
			{/each}
		</Body>
	</Card>
{/if}

<style>
	.category {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: var(--gap1);

		padding: var(--gap2);

		height: 100px;
		width: 100%;
		background: var(--foreground);

		fill: var(--font1);
		border: 2px solid var(--background);
		border-radius: var(--brad1);

		cursor: pointer;

		text-align: center;
		text-transform: capitalize;
	}
	.category:hover {
		border-color: var(--color1);
	}

	:global(.hide_svg + div) {
		font-weight: 600;
	}
	@media screen and (min-width: 600px) {
		.category {
			height: 150px;
		}
	}
</style>
