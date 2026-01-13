<script>
	import Card from '$lib/card.svelte';
	import SVG from '$lib/svg.svelte';
	import Title from '$lib/title.svelte';
</script>

<div id="about" />
<Card>
	<Title card>About Us</Title>

	<section>
		<div class="row_1">
			Meji is your No. 1 trusted online shopping destination in Nigeria. At Meji, we provide you
			with a seamless shopping experience, offering a wide range of products right at your
			fingertips. Whether you're looking for fashion items for men, women, or children, or searching
			for other essentials, we've got you covered.
		</div>

		<div class="row_2">
			<div class="text">
				<SVG icon="change" size="28" />
				<br />
				<span class="bold"> Convenience Delivered </span>

				We understand the value of time and convenience. That's why Meji offers you the ease of
				shopping from anywhere, at any time. Our user-friendly platform allows you to browse and
				purchase your desired items with just a few clicks. Plus, we ensure swift and reliable
				delivery directly to your doorstep.
			</div>

			<div class="vr" />

			<div class="text">
				<SVG icon="offer" size="28" />
				<br />
				<span class="bold"> Secure Payment Solutions </span>

				At Meji, your security is our top priority. With our trusted online shopping payment
				methods, you can enjoy stress-free transactions. We prioritize the safety of your personal
				and financial information, allowing you to shop with peace of mind.
			</div>

			<div class="vr" />

			<div class="text">
				<SVG icon="time" size="28" />
				<br />
				<span class="bold"> 24/7 Services </span>

				We're dedicated to serving you around the clock. Shop online anytime, any day, and
				experience our exceptional customer service. Our team is here to assist you with any
				inquiries or support you may need throughout your shopping journey.
			</div>
		</div>
	</section>
</Card>

<style>
	section {
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.row_1 {
		margin-top: var(--sp2);
	}

	.row_2 {
		display: flex;
		justify-content: center;
		flex-direction: column;
		gap: var(--sp4);

		margin-top: var(--sp5);
		margin-bottom: var(--sp2);

		fill: var(--cl1);
	}

	.row_2 .text {
		display: flex;
		flex-direction: column;
		width: 100%;
	}

	.bold {
		font-weight: 700;
		color: var(--ac1);
		margin-bottom: var(--sp1);
	}

	.vr {
		display: none;
		flex-shrink: 0;

		width: 2px;
		background-color: var(--ac5);
	}

	@media screen and (min-width: 800px) {
		section {
			text-align: center;
		}

		.row_1 {
			max-width: 600px;
		}
		.row_2 {
			flex-direction: unset;
		}

		.row_2 .text {
			max-width: 300px;
			align-items: center;
		}

		.vr {
			display: unset;
		}
	}
</style>
