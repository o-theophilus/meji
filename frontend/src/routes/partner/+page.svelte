<script>
	import { Button } from '$lib/button';
	import { Content, PageTitle } from '$lib/layout';
	import { Icon, Log, Meta } from '$lib/macro';
	import { faqs } from '../faq/faq';
	import Group from '../faq/group.svelte';

	let ops = $state({ open: null });
</script>

<Log entity_type={'page'} />
<Meta
	title="Contact Us"
	description="Get support for your orders, payments, and inquiries — fast, simple, and reliable."
/>

<Content>
	<PageTitle>
		{#snippet title()}
			Have products to sell?
		{/snippet}
		{#snippet copy()}
			Let us help you reach more customers and grow your business.

			<br />
			<br />

			<Button
				--button-background-color="var(--cl1)"
				--button-color="white"
				--button-outline-color="transparent"
				href="/contact"
			>
				Partner with us!
			</Button>
		{/snippet}
	</PageTitle>

	<div class="title">
		If you have quality products and want to increase your sales without worrying about marketing or
		operations, we want you as a partner.
	</div>

	<div class="margin flex">
		<div class="div">
			<div class="title">You might be wondering… how?</div>
			<br />
			<div class="text">
				We bring the customers, you bring the products.
				<br />
				We handle listing, marketing, and sales — so you can focus on supplying while earning consistently.
			</div>
		</div>

		<img src="/image/partner_1.jpg" alt="contact us" />
	</div>

	<div class="margin block bg">
		<div class="title center">Ready to Become a Partner?</div>
		<Button
			--button-background-color="var(--cl1)"
			--button-color="white"
			--button-outline-color="transparent"
			href="/contact"
		>
			Apply Now
		</Button>
	</div>

	<div class="margin">
		<div class="title center">As a Partner, you get</div>

		<div class="card_area">
			<div class="card center">
				<div class="icon">
					<Icon icon="users" size="24"></Icon>
				</div>
				Access to our growing customer base
			</div>
			<div class="card center">
				<div class="icon">
					<Icon icon="trending-up" size="24"></Icon>
				</div>
				Increased sales without running ads
			</div>
			<div class="card center">
				<div class="icon">
					<Icon icon="layout-grid" size="24"></Icon>
				</div>
				Professional product listing & presentation
			</div>
			<div class="card center">
				<div class="icon">
					<Icon icon="package" size="24"></Icon>
				</div>
				Order management handled for you
			</div>
			<div class="card center">
				<div class="icon">
					<Icon icon="wallet" size="24"></Icon>
				</div>
				Reliable payouts
			</div>
			<div class="card center">
				<div class="icon">
					<Icon icon="headset" size="24"></Icon>
				</div>
				Ongoing business support
			</div>
		</div>
	</div>

	<div class="margin title">
		Earn more by reaching customers you wouldn’t normally access — without the stress of selling
		yourself.
	</div>

	<div class="margin flex">
		<div>
			<div class="title">This is perfect for businesses and individuals who:</div>

			<ul>
				<li>Have quality products to supply</li>
				<li>Want to increase sales</li>
				<li>Prefer to focus on production or sourcing</li>
				<li>Need help with marketing and distribution</li>
			</ul>
		</div>

		<img src="/image/partner_2.jpg" alt="contact us" />
	</div>

	<div class="margin">
		<div class="title">FAQ</div>
		{#each faqs as x}
			{#if x.category == 'Partnership'}
				<Group bind:ops category={x}></Group>
			{/if}
		{/each}
	</div>

	<div class="margin center">
		<div class="title">Ready to start selling more?</div>
		<br />
		<Button
			--button-background-color="var(--cl1)"
			--button-color="white"
			--button-outline-color="transparent"
			href="/contact"
		>
			Become a Partner Today
		</Button>
	</div>
</Content>

<style>
	.margin {
		margin: 160px 0;
	}

	.title {
		font-size: 2rem;
		color: var(--ft1);
		line-height: 120%;
		font-weight: 600;
	}

	.center {
		text-align: center;
	}

	img {
		width: 100%;
		border-radius: 8px;
		aspect-ratio: 4/3;
		object-fit: cover;
	}

	.flex {
		display: flex;
		flex-direction: column;
		gap: 24px;

		& > * {
			width: 100%;
		}

		@media screen and (min-width: 580px) {
			flex-direction: row;
			align-items: center;

			& > * {
				width: 50%;
			}
		}
	}

	.block {
		display: flex;

		flex-direction: column;
		align-items: center;
		gap: 24px;

		&.bg {
			padding: 40px 24px;
			border-radius: 8px;
			background-color: var(--bg2);
		}
	}

	.card_area {
		margin-top: 40px;
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 8px;

		@media screen and (min-width: 580px) {
			grid-template-columns: repeat(3, 1fr);
		}

		.card {
			display: flex;
			flex-direction: column;
			align-items: center;
			gap: 16px;

			background-color: var(--bg3);
			padding: 24px 16px;
			border-radius: 8px;

			.icon {
				display: flex;
				justify-content: center;
				align-items: center;
				color: var(--ft2);

				width: 48px;
				aspect-ratio: 1;
				border-radius: 40%;
				background-color: var(--bg1);
			}
		}
	}
</style>
