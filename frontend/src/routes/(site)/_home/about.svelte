<script>
	import { Icon } from '$lib/macro';
</script>

<section id="about">
	<div class="row_1">
		<div class="title">Why buy from Meji</div>
		<div class="text">
			Meji is your No. 1 trusted online shopping destination in Nigeria. At Meji, we provide you
			with a seamless shopping experience, offering a wide range of products right at your
			fingertips. Whether you're looking for fashion items for men, women, or children, or searching
			for other essentials, we've got you covered.
		</div>
	</div>

	<div class="row_2">
		<div class="card">
			<Icon icon="change" size="56" />
			<div class="title">Convenience Delivered</div>
			<div class="text">
				We understand the value of time and convenience. That's why Meji offers you the ease of
				shopping from anywhere, at any time. Our user-friendly platform allows you to browse and
				purchase your desired items with just a few clicks. Plus, we ensure swift and reliable
				delivery directly to your doorstep.
			</div>
		</div>

		<div class="card">
			<Icon icon="offer" size="56" />
			<div class="title">Secure Payment Solutions</div>
			<div class="text">
				At Meji, your security is our top priority. With our trusted online shopping payment
				methods, you can enjoy stress-free transactions. We prioritize the safety of your personal
				and financial information, allowing you to shop with peace of mind.
			</div>
		</div>

		<div class="card">
			<Icon icon="time" size="56" />
			<div class="title">24/7 Services</div>
			<div class="text">
				We're dedicated to serving you around the clock. Shop online anytime, any day, and
				experience our exceptional customer service. Our team is here to assist you with any
				inquiries or support you may need throughout your shopping journey.
			</div>
		</div>
	</div>
</section>

<style>
	section {
		text-align: center;
		margin-top: 120px;
	}

	.row_1,
	.row_2 {
		display: flex;
		justify-content: center;
		flex-direction: column;
		gap: 16px;
	}

	.row_1 {
		padding: 0 16px;
		color: var(--ft1);
		align-items: center;

		& .title {
			font-weight: 800;
			font-size: 2rem;
		}

		& .text {
			font-size: 1.2rem;
			max-width: 740px;
		}
	}
	.row_2 {
		margin-top: 32px;
		flex-direction: column;

		@media screen and (min-width: 800px) {
			& {
				flex-direction: row;
			}
		}

		& .card {
			display: flex;
			flex-direction: column;
			align-items: center;

			background-color: var(--bg3);
			border-radius: 8px;
			padding: 32px;
			/* width: 100%; */
			/* height: 100%; */
			fill: var(--cl1);
			outline: 1px solid var(--ol);
			outline-offset: -1px;
		}

		& .title {
			font-weight: 800;
			font-size: 1.4rem;
			color: var(--ft1);
			margin: 16px 0;
		}

		& .text {
			max-width: 450px;
		}
	}
</style>
