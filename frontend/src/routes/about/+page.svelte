<script>
	import { Button } from '$lib/button';
	import { Content, PageTitle } from '$lib/layout';
	import { Icon, Log, Meta } from '$lib/macro';

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
			A Better Way to Shop
		{/snippet}
		{#snippet copy()}
			Meji is a modern shopping experience built on a simple idea — quality over noise.

			<br />
			<br />
			<Button
				--button-background-color="var(--cl3)"
				--button-background-color-hover="var(--cl3_)"
				--button-color="white"
				--button-outline-color="transparent"
				href="/shop"
				icon2="arrow-right"
			>
				Shop Now
			</Button>
		{/snippet}
	</PageTitle>

	<div class="title">
		In a world of endless options and overwhelming marketplaces, we offer something different: a
		carefully curated collection of products, thoughtfully selected for their design, usefulness,
		and value.
	</div>

	<div class="margin flex reverse">
		<div class="div">
			<div class="title">Our Philosophy</div>
			<br />
			<div class="text">
				We believe shopping should feel effortless, not exhausting.
				<br />
				<br />
				That means:

				<ul>
					<li>No clutter</li>
					<li>No unnecessary choices</li>
					<li>No compromise on quality</li>
				</ul>

				Just products you can trust — presented in a way that respects your time and attention.
			</div>
		</div>

		<img src="/image/about_1.jpg" alt="contact us" />
	</div>

	<div class="margin card_area two mini">
		<div class="card center">
			<div class="icon">
				<Icon icon="target" size="24"></Icon>
			</div>
			<div class="title">Our Mission</div>
			To redefine online shopping through simplicity, clarity, and trust.
		</div>
		<div class="card center">
			<div class="icon">
				<Icon icon="telescope" size="24"></Icon>
			</div>
			<div class="title">Our Vision</div>
			To build a brand people return to — not because they have to, but because they want to.
		</div>
	</div>

	<div class="margin flex">
		<div class="div">
			<div class="title">Our Story</div>
			<br />
			<div class="text">
				Meji was created out of frustration with how complicated online shopping had become.
				<br />
				<br />
				Too many platforms focus on volume instead of value — overwhelming users with choices while offering
				little guidance or assurance.
				<br />
				<br />

				We chose a different path.
				<br />
				<br />

				By focusing on a single, carefully managed store, we maintain complete control over quality,
				presentation, and customer experience.
				<br />
				<br />

				The result is a platform that feels refined, trustworthy, and easy to use.
			</div>
		</div>

		<img src="/image/about_2.jpg" alt="contact us" />
	</div>

	<div class="margin card_area">
		<div class="card center">
			<div class="icon">
				<Icon icon="sparkles" size="24"></Icon>
			</div>
			<div class="bold">Curated Selection</div>
			Every product is intentionally chosen for its quality, design, and real-world usefulness
		</div>
		<div class="card center">
			<div class="icon">
				<Icon icon="badge-check" size="24"></Icon>
			</div>
			<div class="bold">Quality You Can Trust</div>
			Each item is vetted to meet a consistent, high standard
		</div>
		<div class="card center">
			<div class="icon">
				<Icon icon="circle" size="24"></Icon>
			</div>
			<div class="bold">Simplicity First</div>
			No clutter, no overwhelm - just a clean, focused shopping experience
		</div>
		<div class="card center">
			<div class="icon">
				<Icon icon="compass" size="24"></Icon>
			</div>
			<div class="bold">Effortless Discovery</div>
			Find what you need quickly without endless scrolling
		</div>
		<div class="card center">
			<div class="icon">
				<Icon icon="route" size="24"></Icon>
			</div>
			<div class="bold">Seamless Journey</div>
			From browsing to checkout to delivery, everything just flows
		</div>
		<div class="card center">
			<div class="icon">
				<Icon icon="layout-grid" size="24"></Icon>
			</div>
			<div class="bold">Refined Interface</div>
			A fast, modern platform designed to respect your time and attention
		</div>
		<div class="card center">
			<div class="icon">
				<Icon icon="repeat" size="24"></Icon>
			</div>
			<div class="bold">Consistency in Every Order</div>
			Reliable products, predictable quality, every time
		</div>
		<div class="card center">
			<div class="icon">
				<Icon icon="user-check" size="24"></Icon>
			</div>
			<div class="bold">Built Around You</div>
			Designed for people who value efficiency, clarity, and intention
		</div>
		<div class="card center">
			<div class="icon">
				<Icon icon="shield" size="24"></Icon>
			</div>
			<div class="bold">Confidence in Every Choice</div>
			Shop knowing each product has been carefully selected for you
		</div>
	</div>

	<div class="margin block center">
		<div class="title">Looking Ahead</div>

		We are constantly evolving — refining our selection, improving our experience, and raising our
		standards.
		<br />
		<br />
		Because great shopping isn't just about buying things. It's about confidence in every choice you
		make.

		<Button
			--button-background-color="var(--cl3)"
			--button-background-color-hover="var(--cl3_)"
			--button-color="white"
			--button-outline-color="transparent"
			href="/shop"
			icon2="arrow-right"
		>
			Shop Now
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

	.bold {
		font-weight: 600;
		font-size: 1.2rem;
		color: var(--ft1);
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

			&.reverse {
				flex-direction: row-reverse;
			}

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
	}

	.card_area {
		margin-top: 40px;
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 8px;

		@media screen and (min-width: 580px) {
			&:not(.two) {
				grid-template-columns: repeat(3, 1fr);
			}
		}

		&.mini {
			max-width: 800px;
			margin: auto;
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
