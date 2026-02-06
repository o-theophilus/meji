<script>
	import { faqs } from './faq';
	import { Card } from '$lib/layout';
	import { Icon } from '$lib/macro';

	let status = $state(null);
</script>

<!-- TODO: review text -->

<section id="faq">
	<div class="left">
		<span class="page_title">Frequently Asked Questions</span>
		<br />
		<br />
		<span class="text">
			Everything you need to know about shopping, selling, and enjoying the Meji experience
		</span>
	</div>

	<div class="cards">
		{#each faqs as faq, i}
			<Card
				open={status == i}
				onclick={() => {
					if (status == i) {
						status = null;
					} else {
						status = i;
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
		{/each}
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: 24px;

		margin-top: 120px;
		background-color: var(--bg);
		padding: 24px;
		border-radius: 8px;

		@media screen and (min-width: 580px) {
			& {
				flex-direction: unset;
			}
		}

		& .left,
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
