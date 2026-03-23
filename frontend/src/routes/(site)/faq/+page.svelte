<script>
	import { Card, Content, PageTitle } from '$lib/layout';
	import { Log, Meta } from '$lib/macro';
	import Contact from '../contact/contact.svelte';
	import { faqs } from './faq';

	let status = $state(null);
</script>

<Log entity_type={'page'} />
<Meta
	title="FAQ"
	description="Need quick answers? Find solutions to common questions below."
/>

<PageTitle>
	{#snippet title()}
		Frequently Asked Questions
	{/snippet}
	{#snippet copy()}
		Need quick answers? Find solutions to common questions below.
	{/snippet}
</PageTitle>

{#snippet card(faq)}
	<Card
		open={status == faq.q}
		onclick={() => {
			if (status == faq.q) {
				status = null;
			} else {
				status = faq.q;
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

<Content>
	{#each faqs as x}
		<div class="categoty">
			{x.category}
		</div>

		<section>
			<div class="cards">
				{#each x.items as faq, i}
					{#if i % 2 == 0}
						{@render card(faq)}
					{/if}
				{/each}
			</div>

			<div class="cards">
				{#each x.items as faq, i}
					{#if i % 2 != 0}
						{@render card(faq)}
					{/if}
				{/each}
			</div>
		</section>
	{/each}

	<Contact></Contact>
</Content>

<style>
	.categoty {
		margin-top: 52px;
		font-weight: 1.2rem;
		font-weight: 800;
	}
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
