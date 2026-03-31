<script>
	import { Card } from '$lib/layout';

	let { category, ops } = $props();
</script>

{#snippet card(faq)}
	<Card
		open={ops.open == faq.q}
		onclick={() => {
			if (ops.open == faq.q) {
				ops.open = null;
			} else {
				ops.open = faq.q;
			}
		}}
	>
		{#snippet title()}
			<div class="q">
				{faq.q}
			</div>
		{/snippet}
		<div class="a">
			{faq.a}
		</div>
	</Card>
{/snippet}

<section>
	<div class="cards">
		{#each category.items as faq, i}
			{#if i % 2 == 0}
				{@render card(faq)}
			{/if}
		{/each}
	</div>

	<div class="cards">
		{#each category.items as faq, i}
			{#if i % 2 != 0}
				{@render card(faq)}
			{/if}
		{/each}
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: 0 8px;

		@media screen and (min-width: 580px) {
			& {
				flex-direction: unset;
			}
		}

		& .cards {
			width: 100%;
		}
	}

	.cards {
		--card-outline-color: var(--ol);
		--card-title-padding: 12px 16px;
		--card-content-padding: 0 16px 16px 16px;
		--card-background-color: var(--bg3);

		& .q {
			font-weight: 800;
			font-size: 0.9rem;
			color: var(--ft1);
			display: flex;
			align-items: center;
		}

		& .a {
			font-size: 0.8rem;
			color: var(--ft2);
		}
	}
</style>
