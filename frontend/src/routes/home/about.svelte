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
			<div>
				<SVG icon="change" size="28" />
				<br />
				<span> Convenience Delivered </span>
				<p>
					We understand the value of time and convenience. That's why Meji offers you the ease of
					shopping from anywhere, at any time. Our user-friendly platform allows you to browse and
					purchase your desired items with just a few clicks. Plus, we ensure swift and reliable
					delivery directly to your doorstep.
				</p>
			</div>
			<div>
				<SVG icon="offer" size="28" />
				<br />
				<span> Secure Payment Solutions </span>
				<p>
					At Meji, your security is our top priority. With our trusted online shopping payment
					methods, you can enjoy stress-free transactions. We prioritize the safety of your personal
					and financial information, allowing you to shop with peace of mind.
				</p>
			</div>
			<div>
				<SVG icon="time" size="28" />
				<br />
				<span> 24/7 Services </span>
				<p>
					We're dedicated to serving you around the clock. Shop online anytime, any day, and
					experience our exceptional customer service. Our team is here to assist you with any
					inquiries or support you may need throughout your shopping journey.
				</p>
			</div>
		</div>
	</section>
</Card>

<style>
	section {
		display: flex;
		flex-direction: column;
		align-items: center;

		margin: var(--sp4) 0;
		text-align: center;
	}

	.row_1 {
		max-width: 300px;
	}

	.row_2 {
		display: flex;
		justify-content: center;
		flex-direction: column;
		gap: var(--sp4);

		margin: var(--sp4) 0;
		fill: var(--cl1);
	}

	.row_2 div {
		display: flex;
		flex-direction: column;
		align-items: center;

		max-width: 300px;
	}

	span {
		font-weight: 700;
		color: var(--ac1);
	}

	@media screen and (min-width: 800px) {
		.row_2 {
			flex-direction: unset;
		}
		.row_2 div {
			max-width: 200px;
		}
	}
</style>
